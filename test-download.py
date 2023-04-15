#!/usr/bin/env python3

from utils import log, parse_cli, rclone_download

DOWNLOAD_DIR = "test-tree/downloads"

import os
import datetime


def main():
    # Do some initial setup, parse cli, etc
    cli = parse_cli()
    start_time = datetime.datetime.now()
    rclone_download(os.path.join(DOWNLOAD_DIR, cli.remote_dir), cli.remote_dir)
    elapsed_time = datetime.datetime.now() - start_time
    log(f"Last download run completed in {elapsed_time}...")

if __name__ == "__main__":
    main()
