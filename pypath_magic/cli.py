#!/usr/bin/env python
"""
PyPath command-line interface for manipulating the Python path.


"""
import argparse

from .core import PyPath


def get_command_line_args():
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter)
    parser.add_argument('-a', '--add-path', nargs='?', const='',
                        help="Add path to Python path.")
    parser.add_argument('-d', '--delete-path', nargs='?', const='',
                        help="Delete path from user path.")
    parser.add_argument('-l', '--list-all-paths', action='store_true',
                        help="List all paths in Python path.")
    parser.add_argument('-p', '--print-path-file', action='store_true',
                        help="Print path to user's path file.")

    return parser.parse_args()


def main():
    args = get_command_line_args()
    pypath_cmd = PyPath()

    if args.add_path is not None:
        pypath_cmd.add_path(args.add_path)
    elif args.delete_path is not None:
        pypath_cmd.delete_path(args.delete_path)
    elif args.list_all_paths:
        pypath_cmd.list_all_paths()
    elif args.print_path_file:
        pypath_cmd.print_path_file()
    else:
        pypath_cmd.list_custom_paths()


if __name__ == '__main__':
    main()
