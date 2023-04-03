import os
import argparse
import requests
from dotenv import load_dotenv


def count_clicks(link: str, headers: dict) -> str:
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def shorten_link(link: str, headers: dict) -> str:
    data = {"long_url": link,
            'Content-Type': 'application/json',
            }
    url = "https://api-ssl.bitly.com/v4/shorten"
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["link"]


def main(link: str, headers: dict) -> str:
    if not link.startswith("bit.ly"):
        return shorten_link(link, headers)
    return count_clicks(link, headers)


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Получение коротких ссылок')
    parser.add_argument("link", help="Ссылка")
    link = parser.parse_args().link
    headers = {"Authorization": os.getenv("TOKEN")}
    try:
        print(main(link, headers))
    except requests.exceptions.HTTPError as error:
        exit(f"Can't get data from server:\n {error}")
