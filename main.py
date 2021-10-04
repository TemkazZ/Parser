import json
from bs4 import BeautifulSoup
import requests


class TravelParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Accept-Language': 'ru',
        }

    def parse_block(self, item):
        content = {}
        # Название
        div_title = item.find('a', {'class': 'title'})
        title = div_title.find('span', {'class': 'main'}).get_text()
        title = title.replace('\n', '')
        # Цена
        try:
            prices = item.find('div', {'class': 'price'})
            price = prices.get_text()
            price = price.replace(' ', '').replace('\n', '')
        except Exception:
            price = 'нет данных'

        content.update(
            {'Название': title,
             'Цена': price
             }, )

        return content

    def get_page(self, page: int = None):
        params = {}
        if page and page > 1:
            params['page='] = page

        html = self.session.get(
            "https://aptekanevis.ru/catalog/optika/",
            params=params)

        with open("text.html", 'w', encoding='utf-8') as f:
            f.write(html.text)
        with open("text.html", encoding='utf-8') as f:
            src = f.read()

        return src

    def get_content(self):
        html = self.get_page(1)
        cn = []
        bs = BeautifulSoup(html, features='lxml')
        blocks = bs.findAll('div', {'class': 'itembig'})
        for block in blocks:
            content = self.parse_block(block)
            cn.append(content)
        return cn


def parse_hotels():
    a = TravelParser()
    cn = a.get_content()
    # print (cn)
    if cn != None:
        print("Успешно!")
    else:
        print("Провалено!")
    with open("Apteka.txt", 'w', encoding='utf-8') as f:
        f.write(str(cn).replace("}, ", "}\n"))
    return cn


parse_hotels()