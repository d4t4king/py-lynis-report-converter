#!/usr/bin/env python3
"""
'Data' parent class.
"""

PACKAGE_VERSION = '0.0.1'

from .BasicDataStructures import LynisDetails

@staticmethod
def parse_details(list_data: list, verbose: bool =False) -> list:
    """
    Takes a list of "details[]"    
    """
    outlist = list()
    if not 'list' in str(type(list_data)):
        raise TypeError(f"'parse_details' requires a list of details[].  Got a {str(type(list_data))}")
    else:
        for row in list_data:
            _obj = LynisDetails(row)
            outlist.append(_obj)
    return list(set(outlist))

@staticmethod
def parse_systemd_unit_files(list_data: list, verbose: bool=False) -> list:
    outlist = list()
    if not 'list' in str(type(list_data)):
        raise TypeError(f"'parse_systemd_unit_files' requires a list of systemd_unit_files[].  Got a {str(type(list_data))}")
    else:
        for row in list_data:
            _obj = LynisDetails(row)
            outlist.append(_obj)
    return list(set(outlist))

def _test():
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    deets = LynisDetails("FOO-12324, systemd, 'This is a bogus check with bogus data.', 1")
    pp.pprint(deets)

if __name__=='__main__':
    _test()
