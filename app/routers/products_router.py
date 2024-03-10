import json
from typing import Optional

import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException

Products_router = APIRouter(tags=['Products Routers'], prefix='/products')


@Products_router.get("/items")
async def get_items(url: Optional[str] = 'https://www.poizon.com/search?keyword=Nike'):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', type='application/ld+json')
        products_data = []

        for script in scripts:
            script_content = script.string.strip()
            json_ = json.loads(script_content)

            if '@type' in json_ and json_['@type'] == 'ItemList' and 'itemListElement' in json_:
                for product in json_['itemListElement']:
                    name = product['name']
                    price = product['offers']['price']
                    image = product['image']
                    products_data.append({
                        'Name': name,
                        'USDPrice': price,
                        'Image': image
                    })

        return products_data

    else:
        raise HTTPException(status_code=404, detail="Ошибка: Невозможно получить данные с указанного URL")


@Products_router.get("/brands/")
async def get_brands(url: Optional[str] = 'https://www.poizon.com/category/sneakers/skateboarding-500000370'):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', id='__NEXT_DATA__')

        for script in scripts:
            script_content = script.string.strip()
            json_ = json.loads(script_content)

            if 'facets' in json_['props']['pageProps']:
                facets = json_['props']['pageProps']['facets']
                categories_data = []

                for facet in facets:
                    if facet['key'] == 'brandIds':
                        for item in facet['items']:
                            name = item['name']
                            count = item['count']
                            categories_data.append({
                                'Name': name,
                                'Count': count
                            })
                return categories_data

        raise HTTPException(status_code=404, detail="Ошибка: Не удалось найти категории на указанной странице")

    else:
        raise HTTPException(status_code=404, detail="Ошибка: Невозможно получить данные с указанного URL")


@Products_router.get("/categories/")
async def get_categories(url: Optional[str] = 'https://www.poizon.com/category/sneakers/skateboarding-500000370'):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', id='__NEXT_DATA__')

        for script in scripts:
            script_content = script.string.strip()
            json_ = json.loads(script_content)

            if 'facets' in json_['props']['pageProps']:
                facets = json_['props']['pageProps']['facets']
                categories_data = []

                for facet in facets:
                    if facet['key'] == 'categoryIds':
                        for item in facet['items']:
                            name = item['name']
                            count = item['count']
                            categories_data.append({
                                'Name': name,
                                'Count': count
                            })
                return categories_data

        raise HTTPException(status_code=404, detail="Ошибка: Не удалось найти категории на указанной странице")

    else:
        raise HTTPException(status_code=404, detail="Ошибка: Невозможно получить данные с указанного URL")
