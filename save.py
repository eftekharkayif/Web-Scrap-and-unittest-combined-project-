"""Save scraped book data to CSV."""

import csv
import os

FIELDNAMES = ["title", "price", "rating", "availability"]


def save_to_csv(books, filepath):
    """Write a list of book dicts to a CSV file.

    Creates the parent directory if it doesn't exist.
    Writes just the header row if books is empty.
    """
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for book in books:
            writer.writerow(book)

    return filepath
