# cli.py

import argparse

from config import START_URL, OUTPUT_FILENAME
from scrape import crawl_category, get_all_categories
from storage import save_books_to_csv

 # main() will be called from main.py.
def main():

    # Create an ArgumentParser object.
    # description: shown when user runs: python main.py -h
    parser = argparse.ArgumentParser(
        description="Scrape books from books.toscrape.com."
    )

   # Define a command-line argument: --category
    # - type=str: it expects a string value, e.g. --category "Travel"
    # - help: help text shown in -h, and explains default behavior.
    # If user does NOT give --category, we will later default to "sequential art".
    parser.add_argument(
        "--category",
        type=str,
        help="Category name to scrape (case-insensitive). "
             "If omitted, default is 'Sequential Art'.",
    )


    # Define a flag: --all
    # - action="store_true": means this is a boolean flag.
    #   If the user types --all, then args.all == True; otherwise False.
    # This tells the program to scrape EVERY category on the website.
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scrape ALL categories.",
    )


    # Define another argument: --output
    # - type=str: expects a filename string, e.g. --output travel_books.csv
    # If user doesn’t provide this, we will later create a default name.
    parser.add_argument(
        "--output",
        type=str,
        default=OUTPUT_FILENAME,
        help="Output CSV filename. Defaults to the value in config.OUTPUT_FILENAME.",
    )


    # Actually read and parse the command-line arguments.
    # After this:
    # - args.category  -> string or None
    # - args.all       -> True or False
    # - args.output    -> string or None
    args = parser.parse_args()



    # 1. Get all categories from the homepage
    categories = get_all_categories()
    print("Available categories:")
    # Print all category names so the user can see what options exist.
    for name in categories.keys():
        print(" -", name)

    # 2. Decide which URLs to scrape based on the arguments
    if args.all:
        start_urls = list(categories.values())
        label = "all_categories"
    else:
        if args.category:
            choice = args.category.strip().lower()
        else:
            choice = "sequential art"

        if choice not in categories:
            raise ValueError(f"Unknown category: {choice}")

        start_urls = [categories[choice]]
        label = choice.replace(" ", "_")


    # 3. Actually scrape the selected URLs
    all_books = []
    for url in start_urls:
        print(f"\n=== Scraping category URL: {url} ===")
        books = crawl_category(url)
        all_books.extend(books)

        print(f"\nTotal books scraped: {len(all_books)}")
 


    # 4. Decide the output filename
    if args.output and not args.all:
        filename = args.output
    else:
        filename = f"{label}_books.csv"


    
    save_books_to_csv(all_books, filename)