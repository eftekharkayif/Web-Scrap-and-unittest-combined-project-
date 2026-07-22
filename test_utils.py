import unittest

from utils import (
    parse_price,
    parse_rating,
    search_books,
    cheapest_book,
    average_price,
)


class TestParsePrice(unittest.TestCase):
    def test_parses_pound_sign(self):
        self.assertEqual(parse_price("£51.77"), 51.77)

    def test_parses_plain_number_string(self):
        self.assertEqual(parse_price("19.99"), 19.99)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_price("")

    def test_garbage_input_raises(self):
        with self.assertRaises(ValueError):
            parse_price("free!")


class TestParseRating(unittest.TestCase):
    def test_known_word(self):
        self.assertEqual(parse_rating("Three"), 3)

    def test_unknown_word_raises(self):
        with self.assertRaises(ValueError):
            parse_rating("Banana")

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            parse_rating("")


class TestSearchBooks(unittest.TestCase):
    def setUp(self):
        self.books = [
            {"title": "The Great Gatsby", "price": 10.0},
            {"title": "great expectations", "price": 8.0},
            {"title": "1984", "price": 12.0},
        ]

    def test_case_insensitive_match(self):
        results = search_books(self.books, "great")
        self.assertEqual(len(results), 2)

    def test_no_match_returns_empty(self):
        self.assertEqual(search_books(self.books, "nonexistent"), [])

    def test_empty_keyword_returns_all(self):
        self.assertEqual(len(search_books(self.books, "")), 3)


class TestCheapestBook(unittest.TestCase):
    def test_finds_minimum(self):
        books = [{"title": "A", "price": 20.0}, {"title": "B", "price": 5.0}]
        self.assertEqual(cheapest_book(books)["title"], "B")

    def test_empty_list_returns_none(self):
        self.assertIsNone(cheapest_book([]))


class TestAveragePrice(unittest.TestCase):
    def test_computes_average(self):
        books = [{"price": 10.0}, {"price": 20.0}]
        self.assertEqual(average_price(books), 15.0)

    def test_empty_list_returns_zero(self):
        self.assertEqual(average_price([]), 0.0)


if __name__ == "__main__":
    unittest.main()
