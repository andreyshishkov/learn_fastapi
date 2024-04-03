from fastapi import FastAPI
from sample_of_products import sample_products


app = FastAPI()


@app.get('/product/{product_id}')
async def get_product_by_id(product_id: int):
    for product in sample_products:
        if product_id == product['product_id']:
            return product
    return {
        'message': 'Unexisted ID, try another',
    }


@app.get('/products/search')
async def get_product(keyword: str, category: str | None, limit: int = 10):
    response = []
    for product in sample_products:
        if category == product['category'] and keyword in product['name']:
            response.append(product)
    return response[:limit]
