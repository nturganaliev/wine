import os
import collections
import datetime
import pandas as pd

from dotenv import load_dotenv
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def correct_year_name(year):
    lifetime = datetime.date.today().year - year
    if lifetime % 10 == 1:
        year_text = "год"
    elif lifetime % 10 in (2,3,4):
        year_text = "года"
    else:
        year_text = "лет"
    return f'{lifetime} {year_text}'


def categorize_products(filepath):
    products = pd.read_excel(filepath)
    products = products.fillna('')
    products = products.to_dict(orient="records")
    category_dict_of_lists = collections.defaultdict(list)
    for product in products:
        category_dict_of_lists[product['Категория']].append(product)
    return category_dict_of_lists


def main():
    load_dotenv()
    filepath = os.getenv('FILE_PATH')
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    winery_foundation_year = 1920

    template = env.get_template('template.html')

    rendered_page = template.render(
        since = correct_year_name(winery_foundation_year),
        wines = categorize_products(filepath)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()