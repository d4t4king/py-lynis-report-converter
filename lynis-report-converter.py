#!/usr/bin/env python3

import pprint
import argparse
import os
import math

from termcolor import cprint

VERSION = 0.1

def to_bool(val) -> bool:
    if val == 0 or val is None:
        return False
    elif val == 1:
        return True
    else:
        raise Exception("Unrecognized value.  Could not convert to boolean.")
    
def vm_mode(mode: int) -> object:
    if mode == 0:
        return False
    elif mode == 1:
        return 'guest'
    elif mode == 2:
        return 'host'
    else:
        raise Exception("Unrecognized value.  Could not establish VM mode.")
    
def to_long_severity(sev: str) -> object:
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
    
def systemd_uf_status_color(status: str) -> str:
    if status == 'enabled':
        return '#00ff00'
    elif status == 'disabled':
        return '#ff0000'
    elif status == 'static':
        return 'inherit'
    elif status == 'masked':
        return 'goldenrod'
    
def is_prime(num):
    if num <= 1:
        return False
    
    if num == 2:
        return True
    
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
    parser.add_argument('-E', '--excel', dest='excel', required=False, action='store_true', help='Output to Microsoft Excel')
    parser.add_argument('-p', '--pdf', dest='pdf', required=False, action='store_true', help="Output to PDF")
    parser.add_argument('-j', '--json', dest='json', required=False, action='store_true', help='Output in JSON')
    parser.add_argument('-x', '--xml', dest='xml', required=False, action='store_true', help='Output to XML')
    args = parser.parse_args()

    if args.debug:
        args.verbose = True

    if not args.output:
        if args.excel:
            args.output = 'report.xlsx'
        elif args.pdf:
            args.output = 'report.pdf'
        elif args.json:
            args.output = 'report.json'
        elif args.xml:
            args.output = 'report.xml'
        else:
            args.output = 'report.html'

    lynis_log = '/var/log/lynis.log'
    audit_run = False
    lynis_report_date = {}




if __name__=='__main__':
    main()