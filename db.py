from table import Table
from product import Product
from costumer import Costumer
from personnel import Personnel
from sale import Sale
import os

def make_sale(product_id, costumer_id, personnel_id, qty):
    product = products.by_id.get(product_id)
    if qty <= 0:
        raise ValueError("Quantity must be positive")
    if product.qty < qty:
        raise ValueError("Not enough stock")

    sale = sales.add(Sale(0, product_id, costumer_id, personnel_id, qty))
    products.update(product, qty = product.qty - qty)
    return sale


products = Table("products.db", Product)
costumers = Table("costumers.db", Costumer)
personnel = Table("personnel.db", Personnel)
sales = Table("sales.db", Sale)

if os.path.exists(products.path):
    products.loader()
if os.path.exists(costumers.path):
    costumers.loader()
if os.path.exists(personnel.path):
    personnel.loader()
if os.path.exists(sales.path):
    sales.loader()

# products.add(Product(0, "rose", 50, 12))
# products.add(Product(0, "rose", 50, 16))
# products.add(Product(0, "lilium", 35, 20))
# products.show(products.search("rose"))
# costumers.add(Costumer(0, "alex","james"))
# costumers.add(Costumer(0, "kanna", "kamui"))
# personnel.add(Personnel(0, "maya", "rivers", 2000, "night"))
# personnel.add(Personnel(0, "maya", "rivers", 2500, "morning"))
# costumers.show(costumers.search("alex james"))
# personnel.delete(personnel.pick("maya rivers"))
# personnel.show(personnel.search("maya rivers"))
# make_sale(products.pick("rose").id, costumers.pick("alex james").id, personnel.pick("maya rivers").id, 3)
# sales.show(sales.search("2026-10-10"))
# products.show(products.search("rose"))
# sales.show_all()
