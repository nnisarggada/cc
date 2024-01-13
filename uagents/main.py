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

@restock_agent.on_interval(period=5.0)
async def restock_products(ctx: Context):
    for product_id in PRODUCTS.keys():
        product_data = ctx.storage.get(product_id)
        if product_data is None:
            product_status = ProductStatus(
                stock=PRODUCTS[product_id]["stock"],
                restock_amount=PRODUCTS[product_id]["restock_amount"],
                restock_threshold=PRODUCTS[product_id]["restock_threshold"],
                price=PRODUCTS[product_id]["price"],
                category=PRODUCTS[product_id]["category"],
                shelf_life=PRODUCTS[product_id]["shelf_life"],
                dynamic_pricing_factor=PRODUCTS[product_id]["dynamic_pricing_factor"],
            )
            ctx.storage.set(product_id, product_status)
            print(ctx.storage.get(product_id))

        if product_data["stock"] <= product_data["restock_threshold"]:
            request = {"product_id": product_id, "restock_amount": product_data["restock_amount"]}
            await ctx.send("http://127.0.0.1:8000/submit", request)


bureau = Bureau(port=8000, endpoint="http://localhost:8000/submit")
bureau.add(restock_agent)

if __name__ == "__main__":
    bureau.run()

