#!/usr/bin/env python3
import os
import sys
import argparse
from urllib.parse import urlparse
import requests

SPECIAL_FILES_ROOT = "test-tree/special-files/"
LARGE_FILES_PATH = SPECIAL_FILES_ROOT + "large/"
ZIP_FILES_PATH = SPECIAL_FILES_ROOT + "zips/"
CUSTOM_FILES_PATH = SPECIAL_FILES_ROOT + "custom/"
CHUNK_SIZE = 1024 * 1024
LARGE_FILE_URLS = []
ZIP_FILE_URLS = []


def parse_cli():
    """Prepare parser"""
    parser = argparse.ArgumentParser(
        prog="special-files-downloader", description="Download special test files"
    )

    parser.add_argument(
        "--large", help="Download large files for testing", action="store_true"
    )
    parser.add_argument(
        "--zip", help="Download zip files for testing", action="store_true"
    )
    parser.add_argument(
        "--my-source", help="Download files from links listed in text file path"
    )
    parser.add_argument(
        "--all", help="Download all earmarked special files.", action="store_true"
    )

    return parser


def check_paths():
    """Ensure special-file folders required in test-tree are present"""
    if not os.path.exists(SPECIAL_FILES_ROOT):
        os.makedirs(SPECIAL_FILES_ROOT)
    if not os.path.exists(LARGE_FILES_PATH):
        os.makedirs(LARGE_FILES_PATH)
    if not os.path.exists(ZIP_FILES_PATH):
        os.makedirs(ZIP_FILES_PATH)
    if not os.path.exists(CUSTOM_FILES_PATH):
        os.makedirs(CUSTOM_FILES_PATH)


def get_file_urls():
    """Get links to default special-files required for testing"""
    global LARGE_FILE_URLS
    global ZIP_FILE_URLS
    large_files_handle = open("source_large_files.txt", "r", encoding="utf-8")
    large_files = large_files_handle.readlines()
    large_files_handle.close()
    LARGE_FILE_URLS = map(lambda x: x.strip(), large_files)
    zip_files_handle = open("source_zip_files.txt", "r", encoding="utf-8")
    zip_files = zip_files_handle.readlines()
    zip_files_handle.close()
    ZIP_FILE_URLS = map(lambda x: x.strip(), zip_files)


def download_file_from_url(url, path):
    """Download file in url to path"""
    fname = os.path.basename(urlparse(url).path)
    print(f"\nDownloading {fname}\n")
    underline = "=" * len(fname)
    underline = underline + "============"
    print(underline + "\n")
    size = 0
    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            with open(path + fname, "wb") as file:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    file.write(chunk)
                    size = size + (CHUNK_SIZE)
                    print(f"Downloaded {size} bytes of {fname} ...")


def main():
    "Script entry point"
    check_paths()
    get_file_urls()
    parser = parse_cli()
    if len(sys.argv) == 1:
        parser.print_help()
        print(
            "\n========================\n| No downloads done... |\n========================\n"
        )
    args = parser.parse_args()

    if args.large:
        for url in LARGE_FILE_URLS:
            download_file_from_url(url, LARGE_FILES_PATH)
    if args.zip:
        for url in ZIP_FILE_URLS:
            download_file_from_url(url, ZIP_FILE_URLS)
    if args.all:
        ALL_URLS = ZIP_FILE_URLS + LARGE_FILE_URLS
        for url in ALL_URLS:
            download_file_from_url(url, SPECIAL_FILES_ROOT)
    if args.my_source:
        source = open(args.my_source, "r")
        source = source.readlines()
        for url in source:
            download_file_from_url(url.strip(), CUSTOM_FILES_PATH)


if __name__ == "__main__":
    main()
