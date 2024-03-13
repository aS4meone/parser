from fastapi import APIRouter, HTTPException
from typing import Optional

from app.utils.web_parser import get_json_data, parse_product_list, parse_facets

Products_router = APIRouter(tags=['Products Routers'], prefix='/products')


@Products_router.get("/items")
async def get_items(url: Optional[str] = 'https://www.poizon.com/search?keyword=Nike'):
    json_data = get_json_data(url)
    if json_data:
        products_data = parse_product_list(url)
        return products_data
    else:
        raise HTTPException(status_code=404, detail="Ошибка: Невозможно получить данные с указанного URL")


@Products_router.get("/brands/")
async def get_brands(url: Optional[str] = 'https://www.poizon.com/category/sneakers/skateboarding-500000370'):
    json_data = get_json_data(url)
    if json_data:
        brands_data = parse_facets(json_data, 'brandIds')
        return brands_data
    else:
        raise HTTPException(status_code=404, detail="Ошибка: Невозможно получить данные с указанного URL")


@Products_router.get("/categories/")
async def get_categories(url: Optional[str] = 'https://www.poizon.com/category/sneakers/skateboarding-500000370'):
    json_data = get_json_data(url)
    if json_data:
        categories_data = parse_facets(json_data, 'categoryIds')
        return categories_data
    else:
        raise HTTPException(status_code=404, detail="Ошибка: Невозможно получить данные с указанного URL")
