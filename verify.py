#!/usr/bin/env python3
import os
import sys
import hashlib
import argparse

DOWNLOAD_MISC_DIR = "test-tree/downloads/misc"
MISC_DIR = "test-tree/misc"
CHUNK_SIZE = 1024

OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
FAIL = "\033[91m"
WARNING = "\033[93m"
ENDC = "\033[0m"


def hash_file(file_path):
    """ "Make and return SHA-1 hash of file at file_path"""
    h = hashlib.sha1()
    with open(file_path, "rb") as file:
        chunk = 0
        while chunk != b"":
            # read only CHUNK_SIZE bytes at a time
            chunk = file.read(CHUNK_SIZE)
            h.update(chunk)
    return h.hexdigest()


def crawl_upload_and_download_paths():
    """Build a list of uploaded and downloaded paths"""
    uploaded_paths = []
    downloaded_paths = []
    for subdir, _, files in os.walk(MISC_DIR):
        for file in files:
            uploaded_paths.append(os.path.join(subdir, file))

    for subdir, _, files in os.walk(DOWNLOAD_MISC_DIR):
        for file in files:
            downloaded_paths.append(os.path.join(subdir, file))
    return uploaded_paths, downloaded_paths


def make_file_to_harsh_maps():
    uploaded_paths, downloaded_paths = crawl_upload_and_download_paths()
    pre_upload_hashes = []
    post_upload_hashes = []
    for path in uploaded_paths:
        pre_upload_hashes.append({"path": path, "hash": hash_file(path)})
    for path in downloaded_paths:
        post_upload_hashes.append({"path": path, "hash": hash_file(path)})
    return pre_upload_hashes, post_upload_hashes


def parse_cli():
    """Prepare parser"""
    parser = argparse.ArgumentParser(
        prog="verify", description="Check results of upload/download operations"
    )
    parser.add_argument(
        "--misc-complete",
        help="Verify that both the upload and download of the complete misc folder was successful",
        action="store_true",
    )
    parser.add_argument(
        "--nested-complete",
        help="Verify that both the upload and download of the complete nested folder was successful",
        action="store_true",
    )
    parser.add_argument(
        "--succeeded",
        help="Verify that files that were successfully uploaded where downloaded successfully",
        action="store_true",
    )

    return parser


def main():
    parser = parse_cli()
    args = parser.parse_args()
    pre_upload_hash_data, post_upload_hash_data = make_file_to_harsh_maps()
    pre_upload_hashes = map(lambda x: x.get("hash"), pre_upload_hash_data)

    failed_once = False
    if args.succeeded:
        for file_data in post_upload_hash_data:
            print(f"{OKBLUE}Verifying hash for {file_data.get('path')} ...{ENDC}")
            if file_data.get("hash") not in pre_upload_hashes:
                print(
                    f"{WARNING}The hash to the path {file_data.get('path')} is missing!{ENDC}"
                )
                print(
                    f"{WARNING}File has either been modified (on disk or permanent) or is missing!{ENDC}\n"
                )
                failed_once = True
        if not failed_once:
            print(f"{OKGREEN}\nVerification complete!{ENDC}\n")
            print(
                f"{OKGREEN}All downloaded files have matching hashes in pre-uploaded file hashes.{ENDC}\n"
            )
        else:
            print(
                f"{FAIL}\nVerification complete but failed! Missing hash(es) detected.\n{ENDC}"
            )
            print(
                f"{FAIL}At least once missing hash detected, check the logs above.\n{ENDC}"
            )
    elif args.misc_complete:
        pass
    elif args.nested_complete:
        pass
    else:
        print("Not sure what to do!\n\n")
        parser.print_help()


if __name__ == "__main__":
    main()
