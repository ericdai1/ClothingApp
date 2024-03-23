import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re

def get_br_items():
    info_to_scrape = [
        ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045326&nav=meganav%3AMen%3AMen%27s%20Clothing%3APolos', 'men', 'shirt'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045321&nav=meganav%3AMen%3AMen%27s%20Clothing%3ACasual%20Shirts', 'men', 'shirt'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045328&nav=meganav%3AMen%3AMen%27s%20Clothing%3AT-Shirts#department=75', 'men', 'shirt'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045402&nav=meganav%3AMen%3AMen%27s%20Clothing%3AChinos%20%26%20Casual%20Pants#department=75', 'men', 'pants'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1088690&nav=meganav%3AMen%3AMen%27s%20Clothing%3ADress%20Pants', 'men', 'pants'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1068364&nav=meganav%3AMen%3AMen%27s%20Clothing%3AShorts', 'men', 'shorts'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1091674&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3ATops%20%26%20Blouses#department=136', 'women', 'tops'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1044980&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3AT-Shirts%20%26%20Tops#department=136', 'women', 'tops'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045225&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3ADresses', 'women', 'dresses'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045227&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3ASkirts', 'women', 'skirts'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045335&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3APants', 'women', 'pants'),
        # ('https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1105538&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3AShorts', 'women', 'shorts')
    ]

    result = []
    for info in info_to_scrape:
        url = info[0]
        gender = info[1]
        clothing_type = info[2]

        result += get_br_items_per_page(url, gender, clothing_type)

    return result

def get_br_items_per_page(url_to_fetch, gender, clothing_type):
    BR_URL = 'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1145413&nav=meganav%3AMen%3AMen%27s%20Clothing%3AShop%20All%20Men%27s%20Clothing#department=75'
    # Create an HTML session
    session = HTMLSession()

    # Fetch the webpage and render JavaScript. Dynamically scroll through page
    r = session.get(url_to_fetch)
    print('Starting render')
    r.html.render(scrolldown=35, sleep=5)
    print('Finishing render')

    # Access the rendered HTML content
    html_content = r.html.html

    soup = BeautifulSoup(html_content, 'html.parser')

    items = []
    unique_img_urls = set()
    BR_BASE_URL = 'https://bananarepublicfactory.gapfactory.com'

    for item in soup.find_all('div', attrs={'class': re.compile('product-card category-page')}):
        try:
            product_image = item.find('img')
            item_name = product_image.get('alt')
            img_url = product_image.get('src')
            img_url = f'{BR_BASE_URL}{img_url}'

            if img_url in items:
                continue

            store_link = item.find('a').get('href')

            price_info = item.find('span', attrs={'class': re.compile('product-price.*highlight.*')})
            price = float(price_info.get_text(strip=True).split('$')[1])

            unique_img_urls.add(img_url)
            items.append({
                'item_name': item_name,
                'price': price,
                'img_url': img_url,
                'store_link': store_link,
                'gender': gender,
                'clothing_type': clothing_type
            })
        except:
            pass

    return items
