# """Utility functions for parsing and analyzing scraped book data."""


def parse_price(price_text):
    """Convert a price string like '£51.77' into a float.

    Raises ValueError if the string doesn't contain a valid number.
    """
    if not price_text:
        raise ValueError("Price text is empty")

    cleaned = price_text.strip()
    # Strip everything except digits and the decimal point
    cleaned = "".join(ch for ch in cleaned if ch.isdigit() or ch == ".")

    if not cleaned:
        raise ValueError(f"Could not parse price from: {price_text!r}")

    return float(cleaned)


RATING_WORDS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def parse_rating(rating_text):
    """Convert a rating word like 'Three' into an integer (1-5).

    Raises ValueError if the word isn't a recognized rating.
    """
    if not rating_text:
        raise ValueError("Rating text is empty")

    rating_text = rating_text.strip()
    if rating_text not in RATING_WORDS:
        raise ValueError(f"Unknown rating value: {rating_text!r}")

    return RATING_WORDS[rating_text]


def search_books(books, keyword):
    """Return books whose title contains keyword (case-insensitive)."""
    if not keyword:
        return list(books)

    keyword = keyword.lower()
    return [b for b in books if keyword in b["title"].lower()]


def cheapest_book(books):
    """Return the book dict with the lowest price, or None if empty."""
    if not books:
        return None
    return min(books, key=lambda b: b["price"])


def average_price(books):
    """Return the average price of books, or 0.0 if the list is empty."""
    if not books:
        return 0.0
    return sum(b["price"] for b in books) / len(books)
