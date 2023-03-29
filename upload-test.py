#!/usr/bin/env python3

from utils import log, parse_cli, rclone_upload

CHALLENGING_NAMES_DIR = "test-tree/challenging-names"
APOD_DIR = "test-tree/apod"
MISC_DIR = "test-tree/misc"

import os
import sys

gentree = __import__("generate-tree")

def omit_p(fname, omit_list):
    "Return true if fname includes any of the strings in omit_list"
    for o in omit_list:
        if o in fname:
            return True
    return False

def skip_p(fname, cli):
    "Return True if we should skip this file"
    if cli.only != None:
        return not cli.only in fname

    # Skip files if user said to start from a specific file number
    if cli.start != None:
        if not cli.start in fname:
            print(f"Not started yet (waiting on {cli.start}), so skipping {fname}...")
            return True
        cli.start = None

    # Omit files in the omit list
    if cli.omit:
        if omit_p(fname, cli.omit_files):
            print(f"Omitting {fname}...")
            return True

    return False


def main():
    # Do some initial setup, parse cli, etc
    cli = parse_cli()

    if os.path.abspath(cli.directory) == os.path.abspath(CHALLENGING_NAMES_DIR):
        # Step through all the filenames and try to upload each one
        for fname in gentree.fname_permutations():
            if skip_p(fname, cli):
                continue

            # Try to rclone this file
            log(f"Trying {fname}...")
            out = rclone_upload(os.path.join(CHALLENGING_NAMES_DIR, fname), cli.remote_dir)
    elif os.path.abspath(cli.directory) == os.path.abspath(APOD_DIR):
        out = rclone_upload(APOD_DIR, cli.remote_dir, timeout=0)
    elif os.path.abspath(cli.directory) == os.path.abspath(MISC_DIR):
        for fname in os.listdir(MISC_DIR):
            if skip_p(fname, cli):
                continue

            # Try to rclone this file
            log(f"Trying {fname}...")
            out = rclone_upload(os.path.join(MISC_DIR, fname), cli.remote_dir)

            # Upload file 2 twice
            if fname[0:3] == "002":
                out = rclone_upload(os.path.join(MISC_DIR, fname), cli.remote_dir)
    else:
        sys.exit("Not sure what to do with that directory.")


if __name__ == "__main__":
    main()
