import requests
import json
from bs4 import BeautifulSoup

headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

def get_data(r):
    soup = BeautifulSoup(r.content, 'lxml')
    find_names = [" ".join(x.text.split()) for x in soup.find_all('a', 'ProductCardHorizontal__title')]
    find_price = [" ".join(x.text.split()) for x in soup.find_all('span', 'ProductCardHorizontal__price_current-price')]
    links = []
    find_links = soup.find_all('a', 'ProductCardHorizontal__title')
    for x in find_links:
        href = x.get("href")
        link = 'https://www.citilink.ru/' + href
        links.append(link)

    in_one = [{'name': find_names, 'link': links, 'price': find_price} for find_names, links, find_price in
              zip(find_names, links, find_price)]
    return in_one

def CPU():
    r = requests.get(
        url='https://www.citilink.ru/catalog/processory/?f=rating.any%2Cdiscount.price2_5&pf=discount.any%2Crating.any',
        verify=False)

    item = get_data(r)
    print(item)
    with open('CPU_citilink5%.json', 'w', encoding='utf-8') as file:
        json.dump(item, file, indent=4, ensure_ascii=False)


def video_cards():
    r = requests.get(
        url='https://www.citilink.ru/catalog/videokarty/?pf=ms_action%2Cdiscount.any%2Crating.any&f=ms_action%2Crating.any%2Cdiscount.price2_5',
        verify=False)
    item = get_data(r)
    print(item)
    with open('Video_cards_citilink5%.json', 'w', encoding='utf-8') as file:
        json.dump(item, file, indent=4, ensure_ascii=False)


def motherboard():
    r = requests.get(
        url='https://www.citilink.ru/catalog/materinskie-platy/?pf=discount.any%2Crating.any&f=rating.any%2Cdiscount.price2_5',
        verify=False)

    item = get_data(r)
    print(item)
    with open('motherboard_citilink5%.json', 'w', encoding='utf-8') as file:
        json.dump(item, file, indent=4, ensure_ascii=False)


def main():
    pass

if __name__ == "__main__":
    main()
