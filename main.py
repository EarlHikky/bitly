import argparse
import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def count_clicks(link, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def shorten_link(link, headers):
    payload = {"long_url": link}
    url = "https://api-ssl.bitly.com/v4/shorten"
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["link"]


def is_bitlink(link, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}"
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Получение коротких ссылок')
    parser.add_argument("link", help="Ссылка")
    link = parser.parse_args().link
    parsed = urlparse(link)
    bitlink = parsed.netloc + parsed.path
    headers = {"Authorization": os.environ["BITLY_TOKEN"]}
    try:
        if not is_bitlink(bitlink, headers):
            print("Битлинк :", shorten_link(link, headers))
        else:
            print("Количество переходов: ", count_clicks(bitlink, headers))
    except requests.exceptions.HTTPError as error:
        print(f"Can't get data from server:\n {error}")


if __name__ == '__main__':
    main()
