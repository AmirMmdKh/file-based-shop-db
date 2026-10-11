import struct


class Product:
    FIELDS = ("name", "id", "qty", "price")
    FORMAT =  "<i30sii"
    SIZE = struct.calcsize(FORMAT)
    
    def __init__(self, id, name, qty, price, rec = None):
        self.id = id
        self.name = name.lower()
        self.qty = qty
        self.price = price
        self.rec = rec
        self.validation()
        
    def __repr__(self):
        return f"""
    id = {self.id}
    name = {self.name}
    qty = {self.qty}
    price = {self.price}
    """
    
    def to_bytes(self):
        return struct.pack(self.FORMAT, self.id, self.name.encode(),
                           self.qty, self.price)
    
    @classmethod
    def from_bytes(cls, data, rec):
        id, name, qty, price = struct.unpack(cls.FORMAT, data)
        return cls(id, name.rstrip(b"\x00").decode(), qty, price, rec)
    
    def validation(self):
        self.name = self.name.lower()
        if len(self.name.encode()) > 30:
            raise ValueError("Name is too long (maximum 30 bytes)")
        if self.qty < 0:
            raise ValueError("Quantity can't be negative")
        if self.price < 0:
            raise ValueError("Price can't be negative")