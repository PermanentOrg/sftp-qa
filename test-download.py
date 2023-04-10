#!/usr/bin/env python3

from utils import log, parse_cli, rclone_download

DOWNLOAD_DIR = "test-tree/downloads"

import os

def main():
    # Do some initial setup, parse cli, etc
    cli = parse_cli()
    rclone_download(os.path.join(DOWNLOAD_DIR, cli.remote_dir), cli.remote_dir)

if __name__ == "__main__":
    main()
