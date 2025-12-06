import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

 
from config import (
    START_URL,
    USER_AGENT,
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
    OUTPUT_FILENAME,
)
from storage import save_books_to_csv

 
session = requests.Session()
session.headers.update({
    "User-Agent": USER_AGENT
})


def parse_book(article, page_url):
    # get information of one book
    title = article.h3.a["title"].strip()
    price_text = article.select_one("div.product_price p.price_color").text.strip()
    price = re.sub(r'^[^\d]+', '', price_text)
    availability = article.select_one("p.instock.availability").text.strip()
    rating = article.select_one("p.star-rating")["class"][1]  # get stars

    detail_href = article.h3.a["href"]
    detail_url = urljoin(page_url, detail_href)

    img_src = article.select_one("div.image_container img")["src"]
    img_url = urljoin(page_url, img_src)

    return {
        "title": title,
        "price": f"£{price}",
        "availability": availability,
        "rating": rating,
        "detail_url": detail_url,
        "image_url": img_url,
    }


def crawl_category(start_url):
    url = start_url
    books = []

    while url:
        print(f"Crawling: {url}")
        res = session.get(url, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        # for all books
        for article in soup.select("article.product_pod"):
            books.append(parse_book(article, url))

        # next page
        next_link = soup.select_one("li.next a")
        if next_link:
            next_href = next_link["href"]           # "page-2.html"
            url = urljoin(url, next_href)           # build new page
            time.sleep(REQUEST_DELAY)                
        else:
            url = None

    return books

 
