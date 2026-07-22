import unittest
from unittest.mock import patch, Mock

import requests
from bs4 import BeautifulSoup

from scraper import parse_book, scrape_page, fetch_page

SAMPLE_HTML = """
<html><body>
<article class="product_pod">
  <h3><a title="A Sample Book" href="a-sample-book.html">A Sample Book</a></h3>
  <p class="star-rating Four"></p>
  <div class="product_price">
    <p class="price_color">£23.50</p>
    <p class="availability">In stock</p>
  </div>
</article>
</body></html>
"""

SAMPLE_HTML_MULTI = """
<html><body>
<article class="product_pod">
  <h3><a title="Book One" href="one.html">Book One</a></h3>
  <p class="star-rating Two"></p>
  <div class="product_price">
    <p class="price_color">£10.00</p>
    <p class="availability">In stock</p>
  </div>
</article>
<article class="product_pod">
  <h3><a title="Book Two" href="two.html">Book Two</a></h3>
  <p class="star-rating Five"></p>
  <div class="product_price">
    <p class="price_color">£15.00</p>
    <p class="availability">Out of stock</p>
  </div>
</article>
</body></html>
"""


class TestParseBook(unittest.TestCase):
    def test_parses_single_book(self):
        soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
        article = soup.select_one("article.product_pod")
        book = parse_book(article)

        self.assertEqual(book["title"], "A Sample Book")
        self.assertEqual(book["price"], 23.50)
        self.assertEqual(book["rating"], 4)
        self.assertEqual(book["availability"], "In stock")


class TestScrapePage(unittest.TestCase):
    def test_parses_multiple_books(self):
        soup = BeautifulSoup(SAMPLE_HTML_MULTI, "html.parser")
        books = scrape_page(soup)

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]["title"], "Book One")
        self.assertEqual(books[1]["rating"], 5)

    def test_empty_page_returns_empty_list(self):
        soup = BeautifulSoup("<html><body></body></html>", "html.parser")
        self.assertEqual(scrape_page(soup), [])


class TestFetchPage(unittest.TestCase):
    @patch("scraper.requests.get")
    def test_invalid_url_raises(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("bad url")
        with self.assertRaises(requests.exceptions.RequestException):
            fetch_page("http://this-url-does-not-exist.invalid/")

    @patch("scraper.requests.get")
    def test_http_error_raises(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            fetch_page("https://books.toscrape.com/nonexistent-page/")


if __name__ == "__main__":
    unittest.main()
