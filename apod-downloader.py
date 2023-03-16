#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup as BS
from dateutil import parser as date_parser
import os
import requests
import sys
from typing import List

CACHE_DIR = "apod-cache"
ARCHIVE_ROOT = "https://apod.nasa.gov/apod/"
LOCAL_ARCHIVE = "test-tree/APOD"
START_DATE = "2017-04-07"
END_DATE = "2020-03-01"


def slurp(fname):
    with open(fname, 'rb') as fh:
        return str(fh.read())
        
class Link:
    def __init__(self, timestamp: str, html_url: str, name: str, image_url:str="", explanation:str=""):
        self.name = name
        self.timestamp = date_parser.parse(timestamp)
        self.image_url = image_url
        self.explanation = explanation

        ## These pertain to the webpage specific to this image, not the index as a whole
        self.html_url = html_url
        self.html = ""

    def __str__(self) -> str:
        return f'{self.datestr()}: <a href="{self.html_url}>{self.name}</a><img src="{self.image_url}">'

    def datestr(self) -> str:
        "Return timestamp as a %Y-%m-%d string"
        return self.timestamp.strftime("%Y-%m-%d")

    def fetch_image(self):
        """Ensure image is in cache

        Some html pages have a video instead, and we skip those"""
        if self.image_url == "":
            self.parse_html()
        if self.image_url == "VIDEO":
            return

        ext = os.path.splitext(self.image_url)[1]
        fname = os.path.join(CACHE_DIR,  f"{self.datestr()}{ext}") 

        if os.path.exists(fname):
            return
            
        response = requests.get(self.image_url)
        if response.status_code == 200:
            with open(fname, 'wb') as fh:
                fh.write(response.content)
        else:
            sys.stderr.write(f"Couldn't fetch {self.image_url}. Response code: {response.status_code}\n")
            sys.exit()

    def fetch_html(self) -> str:
        """Grab self.html_url from web or cache, return as string

        Side effect: sets self.html to the same html string we return"""

        fname = os.path.join(CACHE_DIR,  f"{self.datestr()}.html") 
        if os.path.exists(fname):
            self.html = slurp(fname).replace(r"\'", "")
            return slurp(fname).replace(r"\'", "")
            
        # Not in cache, so fetch and store it
        response = requests.get(self.html_url)
        if response.status_code == 200:
            self.html = str(response.content)
            with open(fname, 'wb') as fh:
                fh.write(response.content)
        else:
            sys.stderr.write(f"Couldn't fetch {self.html_url}. Response code: {response.status_code}\n")
            sys.exit()

    def fetch(self):
        self.fetch_html()
        self.parse_html()
        self.fetch_image()

    def parse_html(self):
        if self.html == "":
            sys.stderr.write("Cannot fetch image without first fetching html.  Fetching html now.\n")
            self.fetch_html()

        soup = BS(self.html, features="lxml")
        
        # It's a video, not an image
        if "Video Credit" in self.html:
            self.image_url = "VIDEO"
            return
        iframes = soup.find_all('iframe')
        for iframe in iframes:
            if 'youtube.com' in iframe.get('src'):
                self.image_url = "VIDEO"
                return

        self.image_url = ARCHIVE_ROOT + [s for s in soup.find_all('a') if s.get('href') and s.get('href').startswith("image")][0].get("href")
        # try:
        #     self.image_url = ARCHIVE_ROOT + [s for s in soup.find_all('a') if s.get('href') and s.get('href').startswith("image")][0].get("href")
        # except IndexError:
        #     for l in soup.find_all('a'):
        #         print(l, " -=> ", l.get("href"))
            # raise
        # TODO: parse out explanation
        
def get_archive_html() -> str:
    """Fetch html index of photos from web or disk if available

    During testing, I did `wget 'https://apod.nasa.gov/apod/archivepix.html'` to avoid
    constantly re-downloading that page.  This func lets my
    script DTRT regardless of whether somebody has done
    that.

    The index is the only thing that changes.  Everything else is
    write-once, so we can just cache that forever if we want.
    """
    fname = os.path.join(CACHE_DIR, "archivepix.html")
    if os.path.exists(fname):
        return slurp(fname).replace(r"\'", "")
        # with open(fname, "rb") as fh:
        #     return str(fh.read()).replace(r"\'", "'")

    response = requests.get("https://apod.nasa.gov/apod/archivepix.html")
    return str(response.content).replace(r"\'", "'")


def parse_link(line: str) -> Link:
    """Parses a line from the archive and returns a Link object"""
    timestamp, rest = line.split(":", 1)
    anchor = BS(rest, features="lxml").a
    name = anchor.text

    return Link(timestamp, ARCHIVE_ROOT + anchor.get("href"), anchor.text)


def get_links() -> List[Link]:
    """Grab the archive from web or disk, parse it for photo links"""
    lines = get_archive_html().split(r"\n")
    lines = [l for l in lines if '<a href="ap' in l]
    links = []
    for line in lines:
        links.append(parse_link(line))
    return links

def parse_cli():
    global START_DATE
    global END_DATE
    
    cli_parser = argparse.ArgumentParser(
        prog="apod-downloader", description="Download test images from NASA", epilog=""
        )
    cli_parser.add_argument("--start", help=f"start date in %Y-%m-%d format (default: {START_DATE}", default=START_DATE)
    cli_parser.add_argument("--end", help=f"start date in %Y-%m-%d format (default: {END_DATE}", default=END_DATE)

    args = cli_parser.parse_args()
    START_DATE = date_parser.parse(args.start)
    END_DATE = date_parser.parse(args.end)
 
    if END_DATE < START_DATE:
        END_DATE = START_DATE
        sys.stderr.write("End date must be after start date, setting end date equal to start date\n")

    return args

def main():
    os.system(f"mkdir -p {CACHE_DIR}")

    cli = parse_cli()
    links = get_links()
    links = [l for l in links if l.timestamp <= END_DATE]
    links = [l for l in links if l.timestamp >= START_DATE]
    for link in links:
        link.fetch()
        print(link)

if __name__ == "__main__":
    main()
