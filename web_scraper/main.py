from typing import Any, List

from bs4 import BeautifulSoup
import requests

from .model import Joker

BELATRO_JOKERS_URL = "https://balatrogame.fandom.com/wiki/Jokers"


def get_html_document(url: str = BELATRO_JOKERS_URL):
    response = requests.get(url)
    return response.text


def download_image(url, save_as):
    response = requests.get(url)
    with open(save_as, 'wb') as file:
        file.write(response.content)


def get_data() -> list[Joker]:
    """
    BS4 documentation - https://tedboy.github.io/bs4_doc/index.html


    :return: list of dictionaries containing all Jokers of Belatro be ballin
    """

    html_document = get_html_document()
    soup = BeautifulSoup(html_document, "html.parser")
    table = soup.find("table", attrs={"class": "fandom-table sortable"})
    rows = table.find_all("tr")

    jokers = []

    # start from 1st row (exclude columns)
    for row in rows[1:]:
        columns = row.find_all('td')

        num = columns[0].get_text().strip()
        name = columns[1].find('img').get('alt')
        link = columns[1].find('a').get('href')
        image = columns[1].find('img').get('data-src').split('.png')[0] + '.png'
        cost = columns[3].get_text().strip()
        rarity = columns[4].find('span', class_='wds-button').get_text().strip()

        joker = Joker(
            num=num,
            name=name,
            link=link,
            image=image,
            rarity=rarity,
            cost=cost,
        )

        jokers.append(joker)

    return jokers
