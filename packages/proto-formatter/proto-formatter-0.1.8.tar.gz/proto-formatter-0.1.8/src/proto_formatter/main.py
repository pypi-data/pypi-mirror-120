import os
import sys
import types
import argparse
from proto_formatter import format_file
from proto_formatter.util import read_file


def _get_proto_files(root_path):
    proto_files = []
    for path, subdirs, files in os.walk(root_path):
        for name in files:
            if name.endswith('.proto'):
                proto_files.append(os.path.join(path, name))
    return proto_files


def get_option_max_length(parser):
    actions = parser._actions
    max_length = 0
    for action in actions:
        for option_string in action.option_strings:
            if max_length < len(option_string):
                max_length = len(option_string)
        if action.choices:
            for parser_name, parser in action.choices.items():
                if max_length < len(parser_name):
                    max_length = len(parser_name)
                for option_string_action in parser._option_string_actions:
                    if max_length < len(option_string_action):
                        max_length = len(option_string_action)

    return max_length


def format_actions(max_length_of_options, actions):
    saboah = 4  # space amount between option and help

    lines = ['general options:']
    for action in actions:
        if action.option_strings:
            fill_spaces_amount = max_length_of_options - len(action.option_strings[0]) + saboah
            line = f"{' ' * 2}{action.option_strings[0]}{' ' * fill_spaces_amount}{action.help}"
            lines.append(line)

    return lines


def make_usage(parser):
    max_length_of_names = get_option_max_length(parser)
    ONE_SPACE = ' '
    indents = 2
    saboah = 4  # space amount between option and help
    option_lines = ["", "general options:"]
    actions = parser._actions
    commands_lines = []
    for action in actions:
        for option_string in action.option_strings:
            fill_spaces_amount = max_length_of_names - len(option_string) + saboah
            line = f"{ONE_SPACE * indents}{option_string}{ONE_SPACE * fill_spaces_amount}{action.help}"
            option_lines.append(line)

        if action.choices:
            for command, sub_parser in action.choices.items():
                fill_spaces_amount = max_length_of_names - len(command) + saboah
                line = f"{ONE_SPACE * indents}{command}{ONE_SPACE * fill_spaces_amount}{sub_parser.description}"
                commands_lines.append(line)
                for action_name, action_value in sub_parser._option_string_actions.items():
                    for option_string in action_value.option_strings:
                        fill_spaces_amount = max_length_of_names - len(option_string) + saboah
                        line = f"{ONE_SPACE * indents}{option_string}{ONE_SPACE * fill_spaces_amount}{action_value.help}"
                        option_lines.append(line)
    content = """
{before_stars}
*  {description}  *
{end_stars}

usage:
  proto_formatter <command> [options]

commands:
"""
    before_stars = "*" * (len(parser.description) + 6)
    end_stars = before_stars
    content = content.format(description=parser.description, before_stars=before_stars, end_stars=end_stars)
    content = content + '\n'.join(commands_lines + option_lines)
    return content


def new_format_usage(self):
    formatter = self._get_formatter()
    # usage
    formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)

    lines = formatter.format_help().split('\n')
    lines[0] = ''  # replace the prefix "usage:"
    return '\n'.join(lines)


def new_format_help(self):
    formatter = self._get_formatter()
    # usage
    formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)

    lines = formatter.format_help().split('\n')
    lines[0] = ''  # replace the prefix "usage:"
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Format protobuf file(s) from a specific target.")  # add_help=False,
    sub_parser = parser.add_subparsers(dest='command')
    format_parser = sub_parser.add_parser('format', description='format protobuf files', add_help=False)
    view_parser = sub_parser.add_parser('view', description="view file", add_help=False)
    view_parser.add_argument(
        "--file",
        type=str,
        help="target protobuf file, only used for command 'view'"
    )
    format_parser.add_argument(
        "--files",
        type=str,
        nargs="+",
        help="target protobuf files need to be formatted."
    )
    format_parser.add_argument(
        "--folder",
        type=str,
        default=os.getcwd(),
        help="target folder or path, default is current folder, all protubuf files under it and its' subdirectories will be formatted."
    )
    format_parser.add_argument(
        "--indents",
        type=int,
        help="the number of indented spaces",
        default=4
    )
    format_parser.add_argument(
        "--top-comment",
        type=bool,
        default=False,
        help="format all comments as top comments(above the target line)"
    )
    format_parser.add_argument(
        "--align-by-equal-sign",
        type=bool,
        default=False,
        help="align the code by equal sign"
    )
    format_parser.add_argument(
        "--flatten",
        type=bool,
        default=False,
        help="flatten nested objects"
    )
    format_parser.add_argument(
        "--comment-max-length",
        type=int,
        default=999999,
        help="the max length of comment line, defalut is 999999."
    )
    usage = make_usage(parser)
    parser.usage = usage
    # patch format_help method to use custom usage message
    parser.format_help = types.MethodType(new_format_help, parser)
    # patch format_usage method to use custom usage message
    parser.format_usage = types.MethodType(new_format_usage, parser)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit(0)

    if args.command == 'format':
        root_path = os.getcwd()
        if args.files:
            proto_files = [os.path.join(root_path, file) for file in args.files]
        elif args.folder:
            proto_files = _get_proto_files(args.folder)
        else:
            proto_files = _get_proto_files(os.getcwd())

        proto_files = list(set(proto_files))  # remove duplicates
        for fp in proto_files:
            print(f"formatting {fp.replace(root_path, '')}")
            format_file(
                fp,
                indents=args.indents,
                top_comment=args.top_comment,
                align_by_equal_sign=args.align_by_equal_sign,
                flatten=args.flatten,
                comment_max_length=args.comment_max_length,
                new_fp=None
            )
        print("Done!")

    if args.command == 'view':
        args = parser.parse_args()
        fp = os.path.join(os.getcwd(), args.file)
        print(read_file(fp))
