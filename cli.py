# cli.py

import argparse

from config import START_URL, OUTPUT_FILENAME
from scrape import crawl_category
from storage import save_books_to_csv


def main():
    parser = argparse.ArgumentParser(
        description="Scrape books from books.toscrape.com (Sequential Art category by default)."
    )

    parser.add_argument(
        "--url",
        type=str,
        default=START_URL,
        help="Start URL of the category page. Defaults to the Sequential Art category.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=OUTPUT_FILENAME,
        help="Output CSV filename. Defaults to the value in config.OUTPUT_FILENAME.",
    )

    args = parser.parse_args()

    print(f"Crawling category: {args.url}")
    books = crawl_category(args.url)
    print(f"Total books: {len(books)}")

    if books:
        save_books_to_csv(books, args.output)
