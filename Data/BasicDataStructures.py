class LynisDetails:
    def __init__(self, data: str, verbose: bool=False):
        self.id = None
        self.svc = None
        self.desc = None
        self.nmn = None
        if verbose:
            print(f"data is a {str(type(data))}")
        if data.count('|'):
        self.id, self.svc, self.desc, self.nmn = data.split('|')

    def to_json(self):
        return {"id": self.id, "service": self.svc, "description": self.desc, "nmn": self.nmn}
    
class LynisSystemdUnitFile:
    def __init__(self, data: str, verbose: bool=False):
        self.name = None
        self.status = None
        self.name, self.status = data.split('|')

    def to_json(self):
        return {"name": self.name, "status": self.status}