#!/usr/bin/env python3

import os
import random
import string
import argparse

QUANTITY = 1000
FILE_NAME_LENGTH = 10
FILE_SIZE = 1  # 1 Byte
ROOT_NAME = "1000-1B"
SPECIAL_FILES_ROOT = "test-tree/special-files/"


def random_string(length=FILE_NAME_LENGTH):
    "Generate random string of specified length"
    return "".join(random.choices(string.ascii_lowercase, k=length))


def parse_cli():
    """Prepare parser"""
    parser = argparse.ArgumentParser(prog="create-files", description="Generate files")
    parser.add_argument("--quantity", help="Number of files to be generated", type=int)
    parser.add_argument("--size", help="Size of each file to be generated", type=int)
    parser.add_argument("--root-name", help="Download zip files for testing")
    return parser.parse_args()


def write_file(path, size):
    """Write file of {size} to {path}"""
    with open(SPECIAL_FILES_ROOT + "/" + path, "wb") as out:
        out.seek((size) - 1)
        out.write(b"\0")


def check_path(path):
    """Make sure given path exists within special files directory"""
    if not os.path.exists(SPECIAL_FILES_ROOT):
        os.makedirs(SPECIAL_FILES_ROOT)
    if not os.path.exists(SPECIAL_FILES_ROOT + "/" + path):
        os.makedirs(SPECIAL_FILES_ROOT + "/" + path)


def main():
    global QUANTITY
    global FILE_SIZE
    global ROOT_NAME
    args = parse_cli()
    if args.quantity:
        QUANTITY = args.quantity
    if args.size:
        FILE_SIZE = args.size
    if args.root_name:
        ROOT_NAME = args.root_name
    check_path(ROOT_NAME)
    for _ in range(0, QUANTITY):
        write_file(ROOT_NAME + "/" + random_string(), FILE_SIZE)


if __name__ == "__main__":
    main()
