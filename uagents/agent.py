from datetime import datetime, timedelta
from pytz import utc
from typing import List
from pydantic import BaseModel

from uagents import Agent, Bureau, Context, Model, Protocol
from typing import Dict, List

class ProductStatus(Model):
    stock: int
    restock_threshold: int
    restock_amount: int
    price: float
    category: str
    shelf_life: int
    dynamic_pricing_factor: float

class QueryStockRequest(Model):
    product_id: str

class QueryStockResponse(Model):
    stock_level: int
    need_restock: bool
    current_price: float

class RestockRequest(Model):
    product_id: str
    restock_amount: int

class RestockResponse(Model):
    success: bool

inventory_proto = Protocol()

@inventory_proto.on_message(model=QueryStockRequest, replies=QueryStockResponse)
async def handle_query_stock(ctx: Context, sender: str, msg: QueryStockRequest):
    product_id = msg.product_id
    product_status = ctx.storage.get(product_id)
    need_restock = product_status.stock <= product_status.restock_threshold

    await ctx.send(sender, QueryStockResponse(stock_level=product_status.stock, current_price=product_status.price))

@inventory_proto.on_message(model=RestockRequest, replies=RestockResponse)
async def handle_restock(ctx: Context, sender: str, msg: RestockRequest):
    product_id = msg.product_id
    product_status = ctx.storage.get(product_id)
    product_status.stock += msg.restock_amount
    ctx.storage.set(product_id, product_status)
    await ctx.send(sender, RestockResponse(success=True))

restock_agent = Agent(
    name="restock",
    seed="restock_agent seed",
)
restock_agent.include(inventory_proto)

inventory_agent = Agent(
    name="inventory",
    seed="inventory_agent seed",
)

inventory_agent.include(inventory_proto)

PRODUCTS = {
    "product1": ProductStatus(
        stock=15,
        restock_threshold=10,
        restock_amount=5,
        price=10.0,
        category="grocery",
        shelf_life=30,
        dynamic_pricing_factor=1.2,
    ),
    "product2": ProductStatus(
        stock=5,
        restock_threshold=8,
        restock_amount=4,
        price=15.0,
        category="vegetables",
        shelf_life=20,
        dynamic_pricing_factor=1.1,
    ),
    "product3": ProductStatus(
        stock=12,
        restock_threshold=15,
        restock_amount=7,
        price=5.0,
        category="fruits",
        shelf_life=25,
        dynamic_pricing_factor=1.3,
    ),
}

bureau = Bureau(port=9000, endpoint="http://localhost:9000/submit")
bureau.add(restock_agent)
bureau.add(inventory_agent)


class Model(BaseModel):
    pass

class ProductStatus(Model):
    stock: int
    restock_threshold: int
    restock_amount: int
    price: float
    category: str
    shelf_life: int
    dynamic_pricing_factor: float

class InventoryManagementSystem:
    def __init__(self):
        self.products = {
            "product1": ProductStatus(
                stock=50,
                restock_threshold=20,
                restock_amount=30,
                price=10.99,
                category="Electronics",
                shelf_life=365,
                dynamic_pricing_factor=1.2,
            ),
            "product2": ProductStatus(
                stock=100,
                restock_threshold=30,
                restock_amount=40,
                price=25.99,
                category="Clothing",
                shelf_life=180,
                dynamic_pricing_factor=1.1,
            ),
            "product3": ProductStatus(
                stock=30,
                restock_threshold=10,
                restock_amount=15,
                price=5.99,
                category="Groceries",
                shelf_life=30,
                dynamic_pricing_factor=1.15,
            ),
            "product4": ProductStatus(
                stock=80,
                restock_threshold=25,
                restock_amount=35,
                price=15.99,
                category="Home Decor",
                shelf_life=365,
                dynamic_pricing_factor=1.3,
            ),
            "product5": ProductStatus(
                stock=60,
                restock_threshold=15,
                restock_amount=25,
                price=8.99,
                category="Toys",
                shelf_life=90,
                dynamic_pricing_factor=1.25,
            ),
        }

    def simulate_restock(self, product_name: str):
        product = self.products.get(product_name)
        if product:
            if product.stock <= product.restock_threshold:
                print(f"Restocking {product_name} by {product.restock_amount} units.")
                product.stock += product.restock_amount
            else:
                print(f"No restock needed for {product_name}.")

    def simulate_sale(self, product_name: str, quantity: int):
        product = self.products.get(product_name)
        if product:
            if product.stock >= quantity:
                print(f"Selling {quantity} units of {product_name}.")
                product.stock -= quantity
                # Simulate dynamic pricing
                discounted_price = product.price * product.dynamic_pricing_factor
                print(f"Discounted Price: {discounted_price}")
            else:
                print(f"Insufficient stock for {product_name}.")

    def simulate_expiry_check(self):
        current_date = utc.localize(datetime.now())
        product_names_to_remove = []

        for product_name in self.products.keys():
            product = self.products[product_name]
            expiry_date = current_date + timedelta(days=product.shelf_life)
            if expiry_date > current_date:
                print(f"{product_name} has expired. Remove from inventory.")
                product_names_to_remove.append(product_name)

        for product_name in product_names_to_remove:
            del self.products[product_name]

if __name__ == "__main__":
    bureau.run()
    inventory_system = InventoryManagementSystem()

    inventory_system.simulate_restock("product1")
    inventory_system.simulate_sale("product2", 10)
    inventory_system.simulate_sale("product3", 35)

    inventory_system.simulate_expiry_check()
