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

def get_data():
    """
    BS4 documentation - https://tedboy.github.io/bs4_doc/index.html


    :return:
    """

    html_document = get_html_document()

    soup = BeautifulSoup(html_document, "html.parser")

    table = soup.find("table", attrs={"class": "fandom-table sortable"})

    rows = table.find_all("tr")

    jokers = []

    # start from 1st row (exclude columns)
    for row in rows[1:]:
        columns = row.find_all('td')

        nr = columns[0].get_text().strip()
        joker_name = columns[1].find('img').get('alt')
        cost = columns[3].get_text().strip()
        rarity = columns[4].find('span', class_='wds-button').get_text().strip()
        image_link = columns[1].find('img').get('data-src').split('.png')[0] + '.png'

        effect = columns[2].get_text().strip()
        unlock_requirement = columns[5].get_text().strip()
        type = columns[6].find('span').get_text().strip()
        activation = columns[7].get_text().strip()

        joker = Joker(pos=nr, name=joker_name, rarity=rarity, cost=cost, image=image_link)

        jokers.append(joker.dict())


    print(jokers)









