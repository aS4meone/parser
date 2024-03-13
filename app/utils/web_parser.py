import json
import requests
from bs4 import BeautifulSoup
from typing import List, Optional


def get_json_data(url: str) -> Optional[dict]:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', id='__NEXT_DATA__')

        for script in scripts:
            script_content = script.string.strip()
            json_data = json.loads(script_content)
            return json_data

    return None


def parse_facets(json_data: dict, key: str) -> List[dict]:
    if 'facets' in json_data['props']['pageProps']:
        facets = json_data['props']['pageProps']['facets']
        data = []

        for facet in facets:
            if facet['key'] == key:
                for item in facet['items']:
                    name = item['name']
                    count = item['count']
                    data.append({
                        'Name': name,
                        'Count': count
                    })
                return data

    return []


def parse_product_list(url: str) -> List[dict]:
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

    return []
