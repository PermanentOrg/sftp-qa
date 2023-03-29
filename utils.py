#!/usr/bin/env python3
import os
import argparse
import datetime
import subprocess
from pathlib import Path
import __main__

RCLONE_REMOTE = "permanent"
ARCHIVE_PATH = ""
TIMEOUT = 5 * 60
LOG_FILE = "log.txt"

RCLONE = subprocess.check_output("which rclone", shell=True).strip().decode("utf-8")


def which(cmd):
    """Return path to cmd"""
    return subprocess.check_output(f"which {cmd}", shell=True).strip().decode("utf-8")


def log(msg, echo=True):
    """Print message to log file (and screen if echo is True)"""
    if echo:
        print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as fh:
        fh.write(msg)
        fh.write("\n")


def slurp_if_e(fname):
    if os.path.exists(fname):
        with open(fname, encoding="utf-8") as fh:
            return fh.read()
    return ""


def run(fname, args):
    """Execute rclone command pass in args on path fname"""
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


def rclone_upload(fname, remote_dir, timeout: int = TIMEOUT):
    """Upload to rlcone"""
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
    return run(fname, args)


def rclone_download(fname, remote_dir, timeout: int = TIMEOUT):
    """Download from rclone"""
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
            f"{RCLONE_REMOTE}:{ARCHIVE_PATH}{remote_dir}",
            fname,
        ]
    )
    return run(fname, args)


def parse_cli():
    global LOG_FILE
    global RCLONE_REMOTE
    global ARCHIVE_PATH

    program = Path(__main__.__file__).stem
    parser = argparse.ArgumentParser(
        prog=program,
        description="QA test Permanent rclone",
        epilog="For challenging-names, id is a 3-digit number.  For apod, it is a date in %Y-%m-%d format.",
    )
    if program == "upload-test":
        parser.add_argument("directory")
    parser.add_argument("--log-file", help=f"path to log file (defaults to {LOG_FILE})")
    parser.add_argument(
        "--omit",
        help="specify file of ids to omit (misc and challenging-names)",
    )
    parser.add_argument("--only", help="only test one file id")
    parser.add_argument(
        "--remote",
        help="Name of configured rclone remote such as permanent-prod or permanent-dev",
    )
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
        log(
            "If the default remote `permanent` is not configured uploads would fail.",
            True,
        )

    return args
