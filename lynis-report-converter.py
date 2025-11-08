#!/usr/bin/env python3

import pprint
import argparse

from termcolor import cprint

def to_bool(val) -> bool:
    if val == 0 or val is None:
        return False
    elif val == 1:
        return True
    else:
        raise Exception("Unrecognized value.  Could not convert to boolean.")
    
def vm_mode(mode: int) -> bool:
    if mode == 0:
        return False
    elif mode == 1:
        return 'guest'
    elif mode == 2:
        return 'host'
    else:
        raise Exception("Unrecognized value.  Could not establish VM mode.")
    

def main():
    pp = pprint.PrettyPrinter(indent=4)

    # Prepare the arguments
    parser = argparse.ArgumentParser()
    vqd = parser.add_mutually_exclusive_group()
    vqd.add_argument('-v', '--verbose', dest='verbose', required=False, action='store_true', help="Add more output.")
    vqd.add_argument('-q', '--quiet', dest='quiet', required=False, action='store_true', help="Suppress all output except critical errors.  (aka \"cron mode\")")
    vqd.add_argument('-d', '--debug', dest='debug', required=False, action='store_true', help='All the output.')
    parser.add_argument('-i', '--input', dest='input', required=False, help="Specify the input file")
    parser.add_argument('-o', '--output', dest='output', required=True, help="The name of the file to write output.")
    parser.add_argument('--version', dest='version', required=False, action='store_true', help='Prints the version and exits')
    parser.add_argument('-E', '--excel', dest='excel', required=False, action='store_true', help='Output to Microsoft Excel')
    parser.add_argument('-p', '--pdf', dest='pdf', required=False, action='store_true', help="Output to PDF")
    parser.add_argument('-j', '--json', dest='json', required=False, action='store_true', help='Output in JSON')
    parser.add_argument('-x', '--xml', dest='xml', required=False, action='store_true', help='Output to XML')
    args = parser.parse_args()



if __name__=='__main__':
    main()