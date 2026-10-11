from db import products, costumers, personnel, sales, make_sale
from product import Product
from costumer import Costumer
from personnel import Personnel

def ask_text(text):
    while True:
        value = " ".join(input(text).split())
        if value:
            return value
        print("Please type something.")
        
def ask_int(num):
    while True:
        try:
            return int(input(num).strip())
        except ValueError:
            print("Please type a whole number")

def ask_field(field, cast):
    hint = " (morning / afternoon / night)" if field == "shift" else ""
    prompt = f"{field}{hint}: "
    return ask_int(prompt) if cast is int else ask_text(prompt)

ENTITIES = {
    "1": {"title": "Products", "table": products, "cls": Product,
          "fields": [("name", str), ("qty", int), ("price", int)],
          "label": "product name"},
    "2": {"title": "Customers", "table": costumers, "cls": Costumer,
          "fields": [("name", str), ("lastname", str)],
          "label": "customer full name (first last)"},
    "3": {"title": "Personnel", "table": personnel, "cls": Personnel,
          "fields": [("name", str), ("lastname", str), ("salary", int), ("shift", str)],
          "label": "employee full name (first last)"},
}

def add_record(entity):
    values = [ask_field(field, cast) for field, cast in entity["fields"]]
    try:
        record = entity["table"].add(entity["cls"](0, *values))
    except ValueError as e:
        print("Error:", e)
        return
    print("Added:", record)
 
 
def find_record(entity):
    name = ask_text(f"Enter {entity['label']}: ")
    record = entity["table"].pick(name)
    if record is None:
        print("Not found.")
    return record
 
 
def search_records(entity):
    name = ask_text(f"Enter {entity['label']}: ")
    matches = entity["table"].search(name)
    if not matches:
        print("Not found.")
        return
    for record in matches:
        print(record)
 
 
def update_record(entity):
    record = find_record(entity)
    if record is None:
        return
    changes = {}
    for field, cast in entity["fields"]:
        text = input(f"New {field} (Enter to keep '{getattr(record, field)}'): ").strip()
        if text == "":
            continue
        try:
            changes[field] = cast(text)
        except ValueError:
            print(f"Invalid {field}, skipped.")
    if not changes:
        print("Nothing to change.")
        return
    try:
        entity["table"].update(record, **changes)
    except ValueError as e:
        print("Error:", e)
        return
    print("Updated:", record)
 
 
def delete_record(entity):
    record = find_record(entity)
    if record is None:
        return
    print(record)
    if input("Delete this record? (y/n): ").strip().lower() != "y":
        print("Cancelled.")
        return
    entity["table"].delete(record)
    print("Deleted.")
 
 
def list_records(entity):
    records = entity["table"].by_id.values()
    if not records:
        print("Nothing here yet.")
        return
    for record in records:
        print(record)
 
 
def entity_menu(entity):
    actions = {"1": add_record, "2": search_records, "3": update_record,
               "4": delete_record, "5": list_records}
    while True:
        print(f"\n--- {entity['title']} ---")
        print("1. Add")
        print("2. Search")
        print("3. Update")
        print("4. Delete")
        print("5. List all")
        print("0. Back")
        choice = input("> ").strip()
        if choice == "0":
            return
        if choice in actions:
            actions[choice](entity)
        else:
            print("Unknown option.")
 
 
 
def describe_sale(sale):
    product = products.by_id.get(sale.product_id)
    customer = costumers.by_id.get(sale.costumer_id)
    seller = personnel.by_id.get(sale.personnel_id)
    return (f"{sale.date} {sale.time}  "
            f"{product.name if product else '(deleted product)'} x{sale.qty}  "
            f"customer: {customer.fullname if customer else '(deleted)'}  "
            f"sold by: {seller.fullname if seller else '(deleted)'}")
 
 
def new_sale():
    product = products.pick(ask_text("Product name: "))
    if product is None:
        print("Product not found.")
        return
    customer = costumers.pick(ask_text("Customer full name (first last): "))
    if customer is None:
        print("Customer not found.")
        return
    seller = personnel.pick(ask_text("Seller full name (first last): "))
    if seller is None:
        print("Employee not found.")
        return
    qty = ask_int("Quantity: ")
    try:
        sale = make_sale(product.id, customer.id, seller.id, qty)
    except ValueError as e:
        print("Error:", e)
        return
    print("Sale recorded:", describe_sale(sale))
 
 
def search_sales():
    date = ask_text("Date (YYYY-MM-DD): ")
    matches = sales.search(date)
    if not matches:
        print("No sales on that date.")
        return
    for sale in matches:
        print(describe_sale(sale))
 
 
def list_sales():
    records = sorted(sales.by_id.values(), key=lambda s: s.rec)
    if not records:
        print("No sales yet.")
        return
    for sale in records:
        print(describe_sale(sale))
 
 
def sales_menu():
    actions = {"1": new_sale, "2": search_sales, "3": list_sales}
    while True:
        print("\n--- Sales ---")
        print("1. New sale")
        print("2. Search by date")
        print("3. List all")
        print("0. Back")
        choice = input("> ").strip()
        if choice == "0":
            return
        if choice in actions:
            actions[choice]()
        else:
            print("Unknown option.")
 
 
 
def main():
    while True:
        print("\n=== Shop ===")
        print("1. Products")
        print("2. Customers")
        print("3. Personnel")
        print("4. Sales")
        print("0. Exit")
        choice = input("> ").strip()
        if choice in ENTITIES:
            entity_menu(ENTITIES[choice])
        elif choice == "4":
            sales_menu()
        elif choice == "0":
            print("Bye.")
            return
        else:
            print("Unknown option.")
 
 
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye.")