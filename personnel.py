import struct

class Personnel:
    FIELDS = ("name", "lastname", "id", "salary", "shift")
    FORMAT =  "<i30s30si10s"
    SIZE = struct.calcsize(FORMAT)
    SHIFTS = ("morning", "afternoon", "night")
    
    def __init__(self, id, name, lastname, salary, shift, rec = None):
        self.id = id
        self.name = name.lower()
        self.lastname = lastname.lower()
        self.fullname = f"{self.name} {self.lastname}"
        self.salary = salary
        self.shift = shift.lower()
        self.rec = rec
        self.validation()
        
    
    def __repr__(self):
        return f"""
    id = {self.id}
    name = {self.name}
    lastname = {self.lastname}
    salary = {self.salary}
    shift = {self.shift}
    """
    
    def to_bytes(self):
        return struct.pack(self.FORMAT, self.id, self.name.encode(),
                           self.lastname.encode(),self.salary, self.shift.encode())
    
    @classmethod
    def from_bytes(cls, data, rec):
        id, name, lastname, salary, shift = struct.unpack(cls.FORMAT, data)
        return cls(id, name.rstrip(b"\x00").decode(), lastname.rstrip(b"\x00").decode(),
                   salary, shift.rstrip(b"\x00").decode(), rec)

    def validation(self):
        self.name = self.name.lower()
        self.lastname = self.lastname.lower()
        self.fullname = f"{self.name} {self.lastname}"
        self.shift = self.shift.lower()
        if len(self.name.encode()) > 30:
            raise ValueError("Name is too long (maximum 30 bytes)")
        if len(self.lastname.encode()) > 30:
            raise ValueError("Lastname is too long (maximum 30 bytes)")
        if self.shift not in Personnel.SHIFTS:
            raise ValueError("Not in shift list (morning, afternoon, night)")
        if self.salary < 0:
            raise ValueError("Salary can't be negative")