# Shop Manager

A console application for managing a small shop: products, customers, personnel and sales. All data is stored in binary files using fixed-size records, with in-memory indexes for fast lookups. It was written as a university database course project, using only the Python standard library.

## Requirements

- Python 3.8 or newer
- No external packages

## Running

```
python menu.py
```

The data files (`products.db`, `costumers.db`, `personnel.db`, `sales.db`) are created automatically the first time you add a record. Run the program from the project folder.

## Features

- **Products**: add, search by name, update, delete, list all
- **Customers**: the same operations, searched by full name
- **Personnel**: the same operations, with salary and shift (morning / afternoon / night)
- **Sales**: record a sale, search sales by date, list all sales

Recording a sale checks that the product, customer and employee exist, checks that there is enough stock, and then reduces the product's quantity.

## How it works

**Fixed-size records.** Every record type has a `struct` format, so each record takes exactly the same number of bytes. A record's position in the file is its index times the record size, which lets the program jump straight to a record to update or delete it.

**Id first.** The first field of every record is its `id`. Deleting a record overwrites that slot with the id `-1` followed by zeros, so no other record moves and every stored position stays valid. The loader skips these slots but still counts them.

**In-memory indexes.** At startup each file is read once. Every table keeps two dictionaries pointing at the same objects:

- `by_id`: id to record
- `by_name`: name to a list of records (names can repeat, so a lookup can return several matches and the program asks which one you mean)

**Unique ids.** Ids are generated with the `secrets` module (9 digits). A global `all_ids` registry makes sure an id is never used by two records, even in different tables.

**Safe updates.** An update is applied to a copy of the record first and validated. Only if that succeeds is the file written and the real object changed, so a rejected update never leaves the data half-changed.

## Project structure

| File | Purpose |
|---|---|
| `table.py` | `Table` class: loading, adding, searching, updating and deleting records, plus the global `all_ids` registry |
| `product.py` | `Product` record |
| `costumer.py` | `Costumer` record |
| `personnel.py` | `Personnel` record |
| `sale.py` | `Sale` record |
| `db.py` | Creates the four tables and loads their data |
| `menu.py` | The console menu |

## Limitations

- Deleted slots are not reused, so the files only grow.
- All data is loaded into memory at startup.
- Writing a sale and reducing the product's stock are two separate file writes, so they are not atomic.
- Name fields are limited to 30 bytes (not characters; non-ASCII text uses more than one byte per character).
- If you change a record layout, delete the old `.db` files, because they can't be read with the new layout.
