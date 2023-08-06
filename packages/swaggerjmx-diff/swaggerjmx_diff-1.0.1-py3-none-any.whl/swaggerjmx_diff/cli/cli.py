#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  8/17/2021 6:49 PM
@Desc    :  Command line.
"""

import argparse
import sys

from swaggerjmx_diff import __description__, __version__
from swaggerjmx_diff.cli.scaffold import init_parser_scaffold, main_scaffold


def main():
    """Parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="show version"
    )
    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_scaffold = init_parser_scaffold(subparsers)

    if len(sys.argv) == 1:
        # swaggerjmx-diff
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-v", "--version"]:
            # swaggerjmx-diff -v
            print(f"{__version__}")
        elif sys.argv[1] in ["-h", "--help"]:
            # swaggerjmx-diff -h
            parser.print_help()
        elif sys.argv[1] == "startproject":
            # swaggerjmx-diff startproject
            sub_parser_scaffold.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if sys.argv[1] == "startproject":
        main_scaffold(args)
