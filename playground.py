from concurrent.futures import ThreadPoolExecutor
import functools
from bs4 import BeautifulSoup
from requests_html import HTMLSession, AsyncHTMLSession
import re
import time

asession = AsyncHTMLSession()
async def render_br_page(url_to_render):
    result = await asession.get(url_to_render)
    await result.html.arender(timeout=60, scrolldown=35, sleep=1)
    return result

urls_to_render = [
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045326&nav=meganav%3AMen%3AMen%27s%20Clothing%3APolos',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045321&nav=meganav%3AMen%3AMen%27s%20Clothing%3ACasual%20Shirts',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045328&nav=meganav%3AMen%3AMen%27s%20Clothing%3AT-Shirts#department=75',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045402&nav=meganav%3AMen%3AMen%27s%20Clothing%3AChinos%20%26%20Casual%20Pants#department=75',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1088690&nav=meganav%3AMen%3AMen%27s%20Clothing%3ADress%20Pants',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1068364&nav=meganav%3AMen%3AMen%27s%20Clothing%3AShorts',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1091674&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3ATops%20%26%20Blouses#department=136',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1044980&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3AT-Shirts%20%26%20Tops#department=136',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045225&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3ADresses',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045227&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3ASkirts',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1045335&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3APants',
    'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1105538&nav=meganav%3AWomen%3AWomen%27s%20Clothing%3AShorts'
]
genders = ['men'] * 6 + ['women'] * 6
clothing_types = ['shirt', 'shirt', 'shirt', 'pants', 'pants', 'shorts', 'tops', 'tops', 'dresses', 'skirts', 'pants', 'shorts']

render_fn_list = [
    functools.partial(render_br_page, url) for url in urls_to_render
]

start = time.time()
results = asession.run(*render_fn_list)
end = time.time()
print(end - start) 

# def get_all_br_items_async(urls_to_render, genders, clothing_types):
#     BR_URL = 'https://bananarepublicfactory.gapfactory.com/browse/category.do?cid=1145413&nav=meganav%3AMen%3AMen%27s%20Clothing%3AShop%20All%20Men%27s%20Clothing#department=75'
#     # Create an HTML session
#     print('HI')

#     # render_fns = list(map(lambda url : render_br_page(url), urls_to_render))
#     # print(*render_fns)
#     results = asession.run(render_br_page())
#     soups = map(lambda result : BeautifulSoup(result.html.html, 'html.parser'), results)

#     items = []
#     unique_img_urls = set()
    
#     count = 0
#     unique_count = 0
#     for index in range(len(soups)):
#         soup = soups[index]
#         gender = genders[index]
#         clothing_type = clothing_types[index]

#         for item in soup.find_all('div', attrs={'class': re.compile('product-card category-page')}):
#             try:
#                 count += 1

#                 product_image = item.find('img')
#                 item_name = product_image.get('alt')
                
#                 partial_img_url = product_image.get('src')
#                 BR_BASE_URL = 'https://bananarepublicfactory.gapfactory.com'
#                 img_url = f'{BR_BASE_URL}{partial_img_url}'

#                 if img_url in unique_img_urls:
#                     continue
                
#                 unique_img_urls.add(img_url)

#                 store_link = item.find('a').get('href')

#                 price_info = item.find('span', attrs={'class': re.compile('product-price.*highlight.*')})
#                 price = float(price_info.get_text(strip=True).split('$')[1])

#                 items.append({
#                     'item_name': item_name,
#                     'price': price,
#                     'img_url': img_url,
#                     'store_link': store_link,
#                     'gender': gender,
#                     'clothing_type': clothing_type
#                 })

#                 unique_count += 1

#             except:
#                 print(f'Encountered error at count - {count}')

#     # for item in items:
#     #     print(item)
#     # print(f'count: {count}, unique count: {unique_count}')
#     return items

# result = get_all_br_items()
