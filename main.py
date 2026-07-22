"""Run the scraper end-to-end: scrape, save, and report stats."""

from scraper import scrape_all
from save import save_to_csv
from utils import search_books, cheapest_book, average_price


def main():
    print("Scraping books.toscrape.com ...")
    books = scrape_all(max_pages=2)  # remove max_pages to scrape the whole site
    print(f"Scraped {len(books)} books.")

    save_to_csv(books, "data/books.csv")
    print("Saved to data/books.csv")

    cheapest = cheapest_book(books)
    if cheapest:
        print(f"Cheapest book: {cheapest['title']} (£{cheapest['price']})")

    print(f"Average price: £{average_price(books):.2f}")

    keyword = input("Search books by keyword (or press Enter to skip): ").strip()
    if keyword:
        matches = search_books(books, keyword)
        print(f"Found {len(matches)} matches:")
        for b in matches:
            print(f"  - {b['title']} (£{b['price']})")


if __name__ == "__main__":
    main()
