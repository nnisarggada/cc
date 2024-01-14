from fastapi import FastAPI, HTTPException
from main import predict_reorder_quantity

app = FastAPI()

@app.get("/fetch")
async def fetch_reorder_quantity(
    product: str,
    date: str,
    stock: float,
    restock_threshold: float,
    price: float,
    category: str,
    shelf_life: float
):
    try:
        passed_user_input = {
            "product": product,
            "date": date,
            "stock": stock,
            "restock_threshold": restock_threshold,
            "price": price,
            "category": category,
            "shelf_life": shelf_life
        }
        prediction = str(predict_reorder_quantity(passed_user_input))
        return {"predicted_reorder_quantity": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
