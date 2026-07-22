"""Scraper for https://books.toscrape.com/"""

import requests
from bs4 import BeautifulSoup

from utils import parse_price, parse_rating

URL = "https://books.toscrape.com/"

def fetch_page(url):
    """Fetch a page and return a BeautifulSoup object.

    Raises requests.exceptions.RequestException on network/HTTP errors.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_book(article):
    """Extract a single book's data from its <article class='product_pod'> tag."""
    title = article.h3.a["title"]

    price_text = article.select_one(".price_color").get_text()
    price = parse_price(price_text)

    rating_classes = article.select_one("p.star-rating")["class"]
    # rating_classes looks like ['star-rating', 'Three']
    rating_word = rating_classes[1] if len(rating_classes) > 1 else ""
    rating = parse_rating(rating_word)

    availability = article.select_one(".availability").get_text(strip=True)

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
    }


def scrape_page(soup):
    """Parse all books on a single page's soup into a list of dicts."""
    articles = soup.select("article.product_pod")
    books = []
    for article in articles:
        try:
            books.append(parse_book(article))
        except ValueError:
            # Skip a book we can't parse cleanly rather than crashing the run
            continue
    return books


def get_next_page_url(soup, current_url):
    """Return the absolute URL of the next page, or None if there isn't one."""
    next_link = soup.select_one("li.next a")
    if not next_link:
        return None
    return requests.compat.urljoin(current_url, next_link["href"])


def scrape_all(start_url=URL, max_pages=None):
    """Scrape books across all (or up to max_pages) pages."""
    books = []
    url = start_url
    pages_scraped = 0

    while url:
        soup = fetch_page(url)
        books.extend(scrape_page(soup))
        pages_scraped += 1

        if max_pages and pages_scraped >= max_pages:
            break

        url = get_next_page_url(soup, url)

    return books


if __name__ == "__main__":
    all_books = scrape_all()
    print(f"Scraped {len(all_books)} books.")
