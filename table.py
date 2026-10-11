import struct
import os
import secrets
import copy

all_ids = {}

class Table:
    def __init__(self, path, record_cls):
        self.path = path
        self.cls = record_cls
        self.by_id = {}
        self.by_name = {}
        
    def __repr__(self):
        return f"{self.by_id}"
        
    def generate_id(self):
        while True:
            id = 100000000 + secrets.randbelow(900000000)
            if id not in all_ids:
                return id
    def name_key(self, record):
        return getattr(record, "fullname", None) or getattr(record, "name", None) or record.date
    
    def add(self, record):
        record.id = self.generate_id()
        record.rec = os.path.getsize(self.path) // self.cls.SIZE if os.path.exists(self.path) else 0
        with open(self.path, "ab") as f:
            f.write(record.to_bytes())
        name = self.name_key(record)
        self.by_name.setdefault(name, []).append(record)
        self.by_id[record.id] = record
        all_ids[record.id] = record
        
        return record

    def loader(self):
        with open(self.path, "rb") as f:
            rec = 0
            while data := f.read(self.cls.SIZE):
                if struct.unpack_from("<i", data)[0] != -1:
                    record = self.cls.from_bytes(data, rec)
                    name = self.name_key(record)
                    self.by_name.setdefault(name, []).append(record)
                    self.by_id[record.id] = record
                    all_ids[record.id] = record
                rec += 1
                
    def search(self, name):
            return self.by_name.get(name)

    def pick(self, name):
        name = name.lower()
        matches = self.by_name.get(name)
        if not matches:
            return None
        if len(matches) == 1:
            return matches[0]
        for m in matches:
            print(m)
            
        try:
            chosen = self.by_id.get(int(input("type the id: ")))
        except ValueError:
            return None
        
        return chosen if chosen in matches else None
        
    def update(self, record, **changes):
        for field in changes:
            if field not in self.cls.FIELDS:
                raise ValueError(f"Can't update '{field}'") 
        old_id = record.id
        old_name = self.name_key(record)
        new_id = changes.get("id")
        if new_id is not None and new_id != old_id and new_id in all_ids:
            raise ValueError("A record with this id already exists")
        
        clone = copy.copy(record)
        for key, value in changes.items():
            setattr(clone, key, value)
        clone.validation()
        
        with open(self.path, "r+b") as f:
            f.seek(clone.rec * clone.SIZE)
            f.write(clone.to_bytes())
            
        record.__dict__.update(clone.__dict__)
        
        name = getattr(record, "fullname", None) or record.name
        if record.id != old_id:
            self.by_id[record.id] = self.by_id.pop(old_id)
            all_ids[record.id] = all_ids.pop(old_id)
        if name != old_name:
            old_list = self.by_name[old_name]
            old_list.remove(record)
            if not old_list:
                del self.by_name[old_name]
            self.by_name.setdefault(name, []).append(record)
            
        return record
    
    def delete(self, record):
        with open(self.path, "r+b") as f:
            f.seek(record.rec * record.SIZE)
            f.write(struct.pack("<i", -1) + b"\x00" * (self.cls.SIZE - 4))
            
        del all_ids[record.id]
        del self.by_id[record.id]
        name = self.name_key(record)
        matches = self.by_name[name]
        matches.remove(record)
        if not matches:
            del self.by_name[name]
            
        return record
    
    def show(self, records):
        for record in records:
            print(record)
    
    def show_all(self):
        for record in self.by_id.values():
            print(record)
            


    