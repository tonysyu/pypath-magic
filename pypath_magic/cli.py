#!/usr/bin/env python
"""
PyPath command-line interface for manipulating a user's Python path.


"""
import argparse
import textwrap
from itertools import chain

from .core import ACTION_DOCSTRINGS, PyPath


ACTION_HELP = """\
add: {add}
delete, del: {delete}
list: {list}
list-all: {list_all}
path-file: {path_file}
""".format(**ACTION_DOCSTRINGS)


def wrap_text(text, width):
    return textwrap.wrap(text, width, subsequent_indent='    ')


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _split_lines(self, text, width):
        # Override `_split_lines` to preserve new-lines in help-text
        lines = text.split('\n')
        lines = chain.from_iterable(wrap_text(text, width) for text in lines)
        return list(lines)


def get_command_line_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=CustomFormatter)
    parser.add_argument('action', nargs='?', default='list', help=ACTION_HELP,
                        choices=['add', 'delete', 'del', 'list', 'list-all',
                                 'path-file'])
    parser.add_argument('path', nargs='?', default='.',
                        help="Path to add or delete.")
    return parser.parse_args()


def main():
    args = get_command_line_args()
    pypath_cmd = PyPath()

    actions = {
        'add': pypath_cmd.add_path,
        'delete': pypath_cmd.delete_path,
        'del': pypath_cmd.delete_path,
        'list': pypath_cmd.list_custom_paths,
        'list-all': pypath_cmd.list_all_paths,
        'path-file': pypath_cmd.print_path_file
    }
    command = actions[args.action]
    command(args.path)


if __name__ == '__main__':
    main()
