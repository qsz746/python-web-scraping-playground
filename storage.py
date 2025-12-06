import csv


def save_books_to_csv(books, filename):
 
    if not books:
        print("No books to save.")
        return filename

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)

    print(f"Saved to {filename}")
    return filename