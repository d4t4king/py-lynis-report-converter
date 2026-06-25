 #-*- encoding: utf-8 -*-

import pprint

class LynisDetails:
    def __init__(self, data: str, verbose: bool=False):
        __pp = pprint.PrettyPrinter()
        self.id = None
        self.svc = None
        self.desc = None
        self.nmn = None
        self.state = None
        if verbose:
            print(f"data is a {str(type(data))}")
        if data.count('|') > 0:
            try:
                if data.count('|') == 2:
                    self.svc, self.state = data.split('|')
                elif data.count('|') == 4:
                    self.id, self.svc, self.desc, self.nmn = data.split('|')
            except ValueError as error:
                if 'not enough values to unpack' in str(error):
                    print(f"INFO :: Separator count in 'data' is {data.count('|')}")
                    __pp.pprint(data)
                    raise error

    def to_json(self):
        return {"id": self.id, "service": self.svc, "description": self.desc, "nmn": self.nmn}
    
class LynisSystemdUnitFile:
    def __init__(self, data: str, verbose: bool=False):
        self.name = None
        self.status = None
        self.name, self.status = data.split('|')

    def to_json(self):
        return {"name": self.name, "status": self.status}