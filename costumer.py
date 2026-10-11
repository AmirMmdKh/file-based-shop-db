import struct

class Costumer:
    FIELDS = ("name", "lastname", "id")
    FORMAT =  "<i30s30s"
    SIZE = struct.calcsize(FORMAT)
    def __init__(self, id, name, lastname, rec = None):
        self.id = id
        self.name = name.lower()
        self.lastname = lastname.lower()
        self.fullname = f"{self.name} {self.lastname}"
        self.rec = rec
        self.validation()
    
    def __repr__(self):
        return f"""
    id = {self.id}
    name = {self.name}
    lastname = {self.lastname}
    """

    def to_bytes(self):
        return struct.pack(self.FORMAT, self.id, self.name.encode(),
                           self.lastname.encode())
    
    @classmethod
    def from_bytes(cls, data, rec):
        id, name, lastname = struct.unpack(cls.FORMAT, data)
        return cls(id, name.rstrip(b"\x00").decode(), lastname.rstrip(b"\x00").decode(), rec)
    
    def validation(self):
        self.name = self.name.lower()
        self.lastname = self.lastname.lower()
        self.fullname = f"{self.name} {self.lastname}"
        if len(self.name.encode()) > 30:
            raise ValueError("Name is too long (maximum 30 bytes)")
        if len(self.lastname.encode()) > 30:
            raise ValueError("Lastname is too long (maximum 30 bytes)")