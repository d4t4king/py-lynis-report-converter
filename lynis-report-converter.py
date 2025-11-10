#!/usr/bin/env python3

import pprint
import argparse
import os
import math
import re

from termcolor import cprint

VERSION = 0.1

def to_bool(val) -> bool:
    """
    Convert a value to boolean
    Returns True if val = 1
    Returns False if val is 0 or None
    """
    if val == 0 or val is None:
        return False
    elif val == 1:
        return True
    else:
        raise Exception("Unrecognized value.  Could not convert to boolean.")
    
def is_empty_or_none(strng: str) -> bool:
    """ Checks if a string is None or empty ('')"""
    if strng is None or not strng:
        return True
    else:
        return False
    
def vm_mode(mode: int) -> object:
    """
    Translates a trinary code to the type of Virtualization device.  
    0 = no virtualization, aka raw metal
    1 = device is a virtual guest
    2 = device is a virtual host
    Again, debatable if this is better as a dict/constant.
    TODO
    """
    if mode == 0:
        # Since None is a concept in python that doesn't exist in perl, maybe this would be better as None?
        return False
    elif mode == 1:
        return 'guest'
    elif mode == 2:
        return 'host'
    else:
        raise Exception("Unrecognized value.  Could not establish VM mode.")
    
def to_long_severity(sev: str) -> object:
    """
    Translates a letter prompt in the report to the long human-readable severity name.
    Debatable if this is better as a dict....or an enum, but I don't think this is how
    enums work in python.  Maybe a constant?
    TODO
    """
    if sev == 'C':
        return 'Critical'
    elif sev == 'S':
        return 'Severe'
    elif sev == 'H':
        return 'High'
    elif sev == 'M':
        return 'Medium'
    elif sev == 'L':
        return 'Low'
    elif sev == 'I':
        return 'Informational'
    elif sev == 'NA':
        return 'N/A'
    else:
        return None
    
def systemd_uf_status_color(status: str) -> object:
    """
    Sets the HTML color for the systemd status
    """
    if status == 'enabled':
        return '#00ff00'
    elif status == 'disabled':
        return '#ff0000'
    elif status == 'static':
        return 'inherit'
    elif status == 'masked':
        return 'goldenrod'
    else:
        return None
    
def is_prime(num):
    """
    Checks if an integer num is a prime number.
    Returns True is num is prime, False otherwise.
    """

    # Prime numbers must be greater than 1
    if num <= 1:
        return False
    
    # 2 is the only even prime number
    if num == 2:
        return True
    
    # All other even numbers are not prime
    if num % 2 == 0:
        return False
    
    # Check for divisibility by odd numbers from 3 up to the square root of num
    # We only need to check up to the square root because if a number has a factor
    # greater than its square root, it must also have a factopr smaller than its square root.
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
        
    return True

def calc_password_complexity_score(lynis_report_data: dict) -> str:
    """
    Converts the flags in the report to a binary number.
    This is more or less verbatim from the perl version, so this may need some tweaking.
    TODO
    """
    if 'password_max_1_credit' in lynis_report_data.keys():
        lc  = '0b0001'
    else:
        lc = '0b0000'
    if 'password_max_u_credit' in lynis_report_data.keys():
        uc = '0b0010'
    else:
        uc = '0b0000'
    if 'password_max_digital_credit' in lynis_report_data.keys():
        n = '0b0100'
    else:
        n = '0b0000'
    if 'password_max_other_credit' in lynis_report_data.keys():
        o = '0b1000'
    else:
        o = '0b0000'

    score = lc + uc + n + o
    return score

def main():
    pp = pprint.PrettyPrinter(indent=4)

    # Prepare the arguments
    parser = argparse.ArgumentParser()
    vqd = parser.add_mutually_exclusive_group()
    vqd.add_argument('-v', '--verbose', dest='verbose', required=False, action='store_true', help="Add more output.")
    vqd.add_argument('-q', '--quiet', dest='quiet', required=False, action='store_true', help="Suppress all output except critical errors.  (aka \"cron mode\")")
    vqd.add_argument('-d', '--debug', dest='debug', required=False, action='store_true', help='All the output.')
    parser.add_argument('-i', '--input', dest='input', required=False, default='/var/log/lynis-report.dat', help="Specify the input file")
    parser.add_argument('-o', '--output', dest='output', required=False, help="The name of the file to write output.")
    parser.add_argument('--version', dest='version', required=False, action='store_true', help='Prints the version and exits')
    fmts = parser.add_mutually_exclusive_group()
    fmts.add_argument('-E', '--excel', dest='excel', required=False, action='store_true', help='Output to Microsoft Excel')
    fmts.add_argument('-p', '--pdf', dest='pdf', required=False, action='store_true', help="Output to PDF")
    fmts.add_argument('-j', '--json', dest='json', required=False, action='store_true', help='Output in JSON')
    fmts.add_argument('-x', '--xml', dest='xml', required=False, action='store_true', help='Output to XML')
    args = parser.parse_args()

    if args.debug:
        args.verbose = True

    if args.excel:
        ext = "xlsx"
        output_format = 'excel'
    elif args.pdf:
        ext = "pdf"
        output_format = 'pdf'
    elif args.json:
        ext = 'json'
        output_format = 'json'
    elif args.xml:
        ext = 'xml'
        output_format = 'xml'
    else:
        ext = 'html'
        output_format = 'html'

    if not args.output:
        args.output = f"report.{ext}"
    else:
        if args.output.count('/') > 0:
            print(f"Output: {args.output}")
            print(f"Basename of Output: {os.path.basename(args.output)}")
            if (os.path.basename(args.output) == '' or os.path.basename(args.output) is None) \
                or os.path.isdir(args.output):
                if args.output[-1] == '/':
                    args.output = f"{args.output}report.{ext}"
                else:
                    args.output = f"{args.output}/report.{ext}"

    lynis_log = '/var/log/lynis.log'
    audit_run = False
    lynis_report_data = {}

    if not args.quiet:
        cprint(f"Outputting report to {args.output}, in ", "green", end="")
        if args.excel:
            cprint("Excel ", "green", end="")
        elif args.pdf:
            cprint(f"PDF ", "green", end="")
        elif args.xml:
            cprint("XML ", "green", end="")
        elif args.json:
            cprint("JSON ", "green", end="")
        else:
            cprint("HTML ", "green", end="")
        cprint("format.", "green")

    # start processing the report/data
    if os.path.exists(args.input):
        with open(args.input, 'r') as ifile:
            for line in ifile:
                if re.match('^#', line):                            # skip commented lines
                    continue
                parts = line.split('=')
                if len(parts) > 2:                                  # errant = somewhere in either the key or the value
                    match = re.search("^(.+?)=(.+)", line)
                    if match:
                        key = match.group(1)
                        value = match.group(2)
                    else:
                        cprint(f"Line did not match: ", "red", end="")
                        print(line)
                else:
                    key, value = line.split("=")
                if is_empty_or_none(value):
                    if output_format == 'excel' or output_format == 'json':
                        value = 'NA'
                    else:
                        value = '&nbsp;'
                if args.verbose:
                    cprint(f"k: {key}, v: {value}", "yellow")
                if key in lynis_report_data.keys():
                    if 'list' in str(type(lynis_report_data[key])):
                        lynis_report_data[key].append(value)
                    else:
                        temp_v = lynis_report_data[key]
                        del lynis_report_data[key]
                        if re.match("(?:&nbsp;|NA)", temp_v):
                            lynis_report_data[key] = [value]
                        else:
                            lynis_report_data[key] = [temp_v, value]
                else:
                    lynis_report_data[key] = value
    else:
        raise FileNotFoundError(f"Could not file input file ({args.input}).")
    
    keys_to_zeroize = ["container", "notebook", "apparmor_enabled", "apparmor_policy_loaded"]
    for k in keys_to_zeroize:
        if lynis_report_data[k] != 1:
            lynis_report_data[k] = 0

    
    
                
    pp.pprint(lynis_report_data)

if __name__=='__main__':
    main()