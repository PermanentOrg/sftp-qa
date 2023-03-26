#!/usr/bin/env python3

RCLONE_REMOTE = "permanent"
ARCHIVE_PATH = ""
CHALLENGING_NAMES_DIR = "test-tree/challenging-names"
APOD_DIR = "test-tree/apod"
MISC_DIR = "test-tree/misc"
TIMEOUT = 5 * 60
LOG_FILE = "log.txt"

import argparse
import datetime
import os
import subprocess
import sys

gentree = __import__("generate-tree")


RCLONE = subprocess.check_output("which rclone", shell=True).strip().decode("utf-8")


def log(msg, echo=True):
    """Print message to log file (and screen if echo is True)"""
    if echo:
        print(msg)
    with open(LOG_FILE, "a") as fh:
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
    global LOG_FILE
    global RCLONE_REMOTE
    global ARCHIVE_PATH

    parser = argparse.ArgumentParser(
        prog="upload-test",
        description="QA test Permanent rclone",
        epilog="For challenging-names, id is a 3-digit number.  For apod, it is a date in %Y-%m-%d format.",
    )
    parser.add_argument("directory")
    parser.add_argument("--log-file", help=f"path to log file (defaults to {LOG_FILE})")
    parser.add_argument(
        "--omit",
        help="specify file of ids to omit (misc and challenging-names)",
    )
    parser.add_argument("--only", help="only test one file id")
    parser.add_argument("--remote", help="Name of configured rclone remote such as permanent-prod or permanent-dev")
    parser.add_argument("--archive-path", help="Archive path in Permanent.")
    parser.add_argument(
        "--remote-dir",
        help="remote subdirectory (defaults to 'test-tree')",
        default="test-tree",
    )
    parser.add_argument("--start", help="id of file to start from")
    parser.add_argument(
        "--timeout",
        help="number of seconds to allow to upload a challenging-names or misc file",
        default=str(TIMEOUT),
    )
    args = parser.parse_args()

    if args.only:
        args.only = f"{int(args.only):03}"
    if args.start:
        args.start = f"{int(args.start):03}"
    if args.log_file:
        LOG_FILE = args.log_file
    if args.omit:
        args.omit_files = slurp_if_e(args.omit).strip().split("\n")
    if args.archive_path:
        ARCHIVE_PATH = args.archive_path
    if args.remote:
        RCLONE_REMOTE = args.remote
    else:
        log("No rclone remote set. Attempting with default remote `permanent`...", True)
        log("If the default remote `permanent` is not configured uploads would fail.", True)

    return args


def rclone(fname, remote_dir, timeout: int = TIMEOUT):
    args = []
    if timeout > 0:
        args.extend(["timeout", str(timeout)])

    args.extend(
        [
            RCLONE,
            "copy",
            "-vv",
            "--size-only",  # server doesn't do mtime
            "--sftp-set-modtime=false",  # server doesn't do mtime
            fname,
            f"{RCLONE_REMOTE}:{ARCHIVE_PATH}{remote_dir}",
        ]
    )

    start_time = datetime.datetime.now()
    try:
        process = subprocess.Popen(
            args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
        )
        while True:
            output = process.stdout.readline().decode("utf-8")
            if output != "":
                log(output.strip())
            if process.poll() is not None:
                break
    except Exception as e:
        log(f"ERROR: {fname} failed\n{e}")
        return None

    elapsed_time = datetime.datetime.now() - start_time
    log(f"Elapsed time to upload {fname}: {elapsed_time}", True)
    log(f"Return code for rcloning {fname}: {process.poll()}", True)

    return process


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
            out = rclone(os.path.join(CHALLENGING_NAMES_DIR, fname), cli.remote_dir)
    elif os.path.abspath(cli.directory) == os.path.abspath(APOD_DIR):
        out = rclone(APOD_DIR, cli.remote_dir, timeout=0)
    elif os.path.abspath(cli.directory) == os.path.abspath(MISC_DIR):
        for fname in os.listdir(MISC_DIR):
            if skip_p(fname, cli):
                continue

            # Try to rclone this file
            log(f"Trying {fname}...")
            out = rclone(os.path.join(MISC_DIR, fname), cli.remote_dir)

            # Upload file 2 twice
            if fname[0:3] == "002":
                out = rclone(os.path.join(MISC_DIR, fname), cli.remote_dir)
    else:
        sys.exit("Not sure what to do with that directory.")


if __name__ == "__main__":
    main()
