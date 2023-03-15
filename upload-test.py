#!/usr/bin/env python3

RCLONE_REMOTE = "permanent-prod"
ARCHIVE_PATH = "/archives/rclone QA 1 (0a0j-0000)/My Files/test-tree"
TEST_TREE = "test-tree/challenging-names"

import argparse
import os
import subprocess
import sys
import simplejson as json
gentree = __import__("generate-tree")


RCLONE = subprocess.check_output("which rclone", shell=True).strip().decode("utf-8")


def log(msg, echo=True):
    """Print message to log file (and screen if echo is True)"""
    if echo:
        print(msg)
    with open("log.txt", "a") as fh:
        fh.write(msg)
        fh.write("\n")


def slurp_if_e(fname):
    if os.path.exists(fname):
        with open(fname) as fh:
            return fh.read()
    return ""


def which(cmd):
    """Return path to cmd"""
    return subprocess.check_output(f"which {cmd}", shell=True).strip().decode("utf-8")


def omit_p(fname, omit_list):
    "Return true if fname includes any of the strings in omit_list"
    for o in omit_list:
        if o in fname:
            return True
    return False


def parse_cli():
    parser = argparse.ArgumentParser(
        prog="upload-test", description="QA test Permanent rclone", epilog=""
    )
    parser.add_argument("--start", help="number of file to start from")
    parser.add_argument(
        "--no-omit", help="turn off skipping file numberss listed in omit.txt"
    )
    args = parser.parse_args()

    if args.start:
        args.start = f"{int(args.start):03}"

    return args

def rclone(fname):
    """Actually do the rclone on this one file

    Returns CompletedProcess object, or none if subprocess throws an exception"""

    args = [
        RCLONE,
        "copy",
        # "--log-level=DEBUG", "--log-file=log.txt",
        "-v",
        "--size-only",
        "--sftp-set-modtime=false",
        os.path.join(TEST_TREE, fname),
        f"{RCLONE_REMOTE}:{ARCHIVE_PATH}",
    ]
    try:
        out = subprocess.run(args, capture_output=True, timeout=60)
    except Exception as e:
        log(f"ERROR: {fname} failed\n{e}")
        return None
    return out

 
def main():
    # Do some initial setup, parse cli, etc
    cli = parse_cli()
    started = cli.start == None
    omit = slurp_if_e("omit.txt").strip().split("\n")

    # Step through all the filenames and try to upload each one
    for fname in gentree.fname_permutations():

        # Skip files if user said to start from a specific file number
        if not started:
            if not cli.start in fname:
                print(f"Not started yet, so skipping {fname}...")
                continue
            started = True

        # Omit files in the omit list
        if not cli.no_omit:
            if omit_p(fname, omit):
                print(f"Omitting {fname}...")
                continue

        # Try to rclone this file
        print(f"Trying {fname}...")
        out = rclone(fname)
        if not out:
            continue

        # Capture success and failure
        msg = {
            "args": out.args,
            "returncode": out.returncode,
            "stderr": out.stderr,
            "stdout": out.stdout,
        }
        log(json.dumps(msg, indent=4), out.returncode != 0)


if __name__ == "__main__":
    main()
