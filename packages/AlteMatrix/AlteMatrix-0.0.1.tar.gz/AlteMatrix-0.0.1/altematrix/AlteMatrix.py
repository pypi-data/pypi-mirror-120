#!/usr/bin/env python3
import argparse
import os
from platform import python_version
import sys
import ascii_text as txt, __init__ as f

cwd = os.getcwd()
if '/' in cwd:
    if '/altematrix' in cwd:red = '/'
    else:red = '/'
elif '\\' in cwd:
    if '\\altematrix' in cwd:red = '\\'
    else:red = '\\'

if python_version()[0:3] < '3.6':
        print('Make sure you have Python 3.6+ installed, quitting.')
        sys.exit(1)

word = "IP ANALYZER"
txt.write(word)

print("Version:",f.__version__)

if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(
        description="CTFtools is used to perform some basic conversions and networking analysis functions for CTFs or pentesting."
    )
    parser.add_argument('module', help='''Module to be run.
                        [converter, ipanalyzer, 2comp]''')

    # Parse arguments
    args = parser.parse_args()

    if args.module == 'converter':
        new = cwd + red + 'converter.py'
        print("Directory:",new)
    elif args.module == 'ipanalyzer':
        new = cwd + red + 'ipanalyzer.py'
        print("Directory:",new)
    elif args.module == '2comp':
        new = cwd + red + 'twos_complement.py'
        print("Directory:",new)
    else:
        print(f"{args.module} module could not be found or does not exist!")
