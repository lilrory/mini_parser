import aiohttp
import asyncio
import sys
from bs4 import BeautifulSoup


async def get_html(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_product_data(session, url):
    html = await get_html(session, url)
    soup = BeautifulSoup(html, 'html.parser')

    brand_elements = soup.find_all('div', class_='catalog-item__brand')
    product_name_elements = soup.find_all('div', class_='catalog-item__title-name')
    price_elements = soup.find_all('span', class_='price--current')

    brand_texts = [brand.text.strip() for brand in brand_elements] if brand_elements else ['No brand found']
    name_texts = [product_name.text.strip() for product_name in product_name_elements] if product_name_elements else ['No title found']
    prices = [price.text.strip() for price in price_elements] if price_elements else ['No price found']

    return brand_texts, name_texts, prices


async def parse_catalog_page(session, base_url, page_num):
    url = f'{base_url}?page={page_num}'
    brand, product_name, prices = await get_product_data(session, url)
    return brand, product_name, prices


async def main():
    base_url = 'https://itkkit.com/catalog/sale/'
    async with aiohttp.ClientSession() as session:
        with open('output.txt', 'w', encoding='utf-8') as output_file:
            sys.stdout = output_file

            max_pages = 3
            for page_num in range(1, max_pages + 1):
                brand, product_name, prices = await parse_catalog_page(session, base_url, page_num)
                for i in range(len(prices)):
                    print(f"{brand[i]} {product_name[i]}: {prices[i]}")

        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    asyncio.run(main())
