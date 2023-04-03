#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from urllib.parse import urlparse

SPECIAL_FILES_PATH = "test-tree/special-files/"
LARGE_FILE_URIS = [
    "https://www.quintic.com/software/sample_videos/Cricket%20Bowling%20150fps%201200.avi"
]
ZIP_FILE_URLS = []


def parse_cli():
    parser = argparse.ArgumentParser(
        prog="special-files-downloader", description="Download special test files"
    )

    parser.add_argument("--large", help=f"Download large files for testing")
    parser.add_argument("--zip", help=f"Download zip files for testing")
    parser.add_argument(
        "--my-sources", help=f"Download files from links listed in text file path"
    )
    parser.add_argument(
        "--all",
        help="Download all earmarked special files.",
    )

    return parser


def download_file_from_url(uri, path):
    response = requests.get(uri, allow_redirects=False)
    fname = os.path.basename(urlparse(uri).path)
    if response.status_code == 200:
        with open(path + fname, "wb") as file:
            file.write(response.content)


def main():
    parser = parse_cli()
    if len(sys.argv) == 1:
        parser.print_help()
        print("No downloads done....")
    args = parser.parse_args()

    if args.large:
        for uri in LARGE_FILE_URIS:
            download_file_from_url(uri, SPECIAL_FILES_PATH + "large/")
    if args.zip:
        for uri in ZIP_FILE_URLS:
            download_file_from_url(uri, SPECIAL_FILES_PATH + "zips/")
    if args.all:
        ALL = ZIP_FILE_URLS + LARGE_FILE_URIS
        for uri in ALL:
            download_file_from_url(uri, SPECIAL_FILES_PATH + "mixed/")
    if args.my_sources:
        sources = open(args.my_sources, "r")
        sources = sources.readlines()
        for source in sources:
            download_file_from_url(source, SPECIAL_FILES_PATH + "custom/")


if __name__ == "__main__":
    main()
