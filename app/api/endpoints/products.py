from typing import List

from fastapi import APIRouter, FastAPI

from app.api.schemas.products import Product
from app.db.products_data import sample_products

# app = FastAPI()
router = APIRouter(prefix='/products', tags=['products'])


@router.get('/{product_id}', response_model=Product)
async def get_product(product_id: int):
    products = sample_products
    for product in products:
        if product['product_id'] == product_id:
            return product


@router.get('/search', response_model=List[Product])
async def search_products(keyword: str, category: str = None, limit: int = 10):
    filtered_products = []

    for product in sample_products:
        keyword_match = keyword.lower() in product['name'].lower()
        category_match = category is None or product['category'].lower() == category.lower()
        if keyword_match and category_match:
            filtered_products.append(product)

    return filtered_products[:limit]