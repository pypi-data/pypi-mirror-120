#!/usr/bin/python3
# -*- coding: utf-8 -*-
r"""
Utility to create an environment.yml file from imports.

Example:

        $ environment_extractor --dir C:\Users\user\Documents\project
        --ignored_libs "pef lightgbm" --name ng
        --channels "pytorch pvlib defaults"
        --extra_libs "fiona geopandas"

MIT License

Copyright (c) 2021 Joshua Brooke

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__ = "Joshua Brooke"
__license__ = "MIT License"
__version__ = "0.1"
__maintainer__ = "Joshua Brooke"
__email__ = "joshua.brooke@outlook.com"
__status__ = "Development"


import argparse
import os
import re
import sys

from stdlib_list import stdlib_list


def main():
    parser = argparse.ArgumentParser(
        description="Generate environment.yml for use with conda"
    )
    parser.add_argument(
        "--dir",
        metavar="directory",
        type=str,
        help="directory containing files to parse",
        required=False,
    )
    parser.add_argument(
        "--name",
        metavar="name",
        type=str,
        help="name of environment for yml file",
        required=False,
    )
    parser.add_argument(
        '--include_stdlib', dest='include_stdlib', action='store_true'
    )

    parser.add_argument(
        "--ignored_libs",
        metavar="ignored_libs",
        type=str,
        help="libraries to ignore, space separated",
        required=False,
    )
    parser.add_argument(
        "--extra_libs",
        metavar="extra_libs",
        type=str,
        help="libraries to add, space separated",
        required=False,
    )
    parser.add_argument(
        "--channels",
        metavar="ignored_libs",
        type=str,
        help="channels for conda to use",
        required=False,
    )
    args = parser.parse_args()

    name = args.name if args.name else ''
    directory = args.dir if args.dir else os.getcwd()
    include_standard_lib = args.include_stdlib
    ignored_libs = args.ignored_libs.split(" ") if args.ignored_libs else []
    extra_libs = args.extra_libs.split(" ") if args.extra_libs else []
    channels = args.channels.split(" ") if args.channels else []

    python_scripts = [
        os.path.join(dp, file)
        for dp, dn, filenames in os.walk(directory)
        for file in filenames
        if os.path.splitext(file)[1] == '.py'
    ]

    imports = []
    for script in python_scripts:
        with open(script, 'r') as f:
            for ln in f:
                if re.match(r'import .', ln) or re.match(r'from .', ln):
                    imports.append(ln)

    # TODO: Make into a Regex
    cleaned_imports = [
        s.replace("import ", "")
        .replace("from ", "")
        .replace("\n", "")
        .split(" ")[0]
        .split(".")[0]
        for s in imports
    ]

    environment_libs = list(dict.fromkeys(cleaned_imports))

    if include_standard_lib is False:
        std_lib = stdlib_list(
            str(sys.version_info[0]) + '.' + str(sys.version_info[1])
        )
        environment_libs = [x for x in environment_libs if x not in std_lib]

    if ignored_libs is not None:
        environment_libs = [
            x for x in environment_libs if x not in ignored_libs
        ]

    if extra_libs is not None:
        environment_libs = extra_libs + environment_libs

    with open(directory + '\\environment.yml', 'w') as f:
        f.write('name: ' + name + '\n')
        f.write('channels: \n')
        for channel in channels:
            f.write('  - ' + channel + '\n')
        f.write('dependencies: \n')
        for element in environment_libs:
            f.write('  - ' + element + '\n')


if __name__ == "__main__":
    main()
