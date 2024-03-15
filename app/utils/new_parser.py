import requests
from bs4 import BeautifulSoup


def scrape_poizon_data(url: str) -> dict:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        goods_div = soup.find('div', class_='GoodsList_goodsList__hPoCW')

        if goods_div:
            products_data = []
            product_tags = goods_div.find_all('a', class_='GoodsItem_goodsItem__pfNZb')

            for tag in product_tags:
                product_link = "https://www.poizon.com" + tag['href']
                product_name = tag.find('div', class_='GoodsItem_spuTitle__ED79N').text.strip()
                product_image = tag.find('img')['src']
                product_price = tag.find('div', class_='GoodsItem_money__2aMgt').text.strip()

                products_data.append({
                    'Link': product_link,
                    'Name': product_name,
                    'Image': product_image,
                    'USDPrice': product_price
                })

            return {"products": products_data}
        else:
            return {"message": "Див с классом 'GoodsList_goodsList__hPoCW' не найден на странице."}
    else:
        return {"message": "Ошибка при выполнении запроса на веб-страницу."}
