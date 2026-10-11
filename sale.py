import struct
import datetime

class Sale:
    FIELDS = ["qty"]
    FORMAT =  "<i10s8siiii"
    SIZE = struct.calcsize(FORMAT)
    
    def __init__(self, id, product_id, costumer_id, personnel_id, qty, rec = None, date = None, time = None):
        now = datetime.datetime.now()
        self.id = id
        self.date = date or now.strftime("%Y-%m-%d")
        self.time = time or now.strftime("%H:%M:%S")
        self.product_id = product_id
        self.costumer_id = costumer_id
        self.personnel_id = personnel_id
        self.qty = qty
        self.rec = rec
        self.validation()
        
    def __repr__(self):
        return f"""
        id = {self.id}
        date = {self.date}
        time = {self.time}
        product_id = {self.product_id}
        costumer_id = {self.costumer_id}
        personnel_id = {self.personnel_id}
        qty = {self.qty}
        """

    def to_bytes(self):
        return struct.pack(self.FORMAT, self.id, self.date.encode(), self.time.encode(),
                           self.product_id, self.costumer_id, self.personnel_id, self.qty)
        
    @classmethod
    def from_bytes(cls, data, rec):
        id, date, time, product_id, costumer_id, personnel_id, qty = struct.unpack(cls.FORMAT, data)
        return cls(id, product_id, costumer_id, personnel_id, qty, rec,
                   date.rstrip(b"\x00").decode(), time.rstrip(b"\x00").decode())
        
    def validation(self):
        if self.qty < 0:
            raise ValueError("Quantity can't be negative")
            
    