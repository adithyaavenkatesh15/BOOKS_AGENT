#
import requests


def book_search(query, api_key):
    """
    Search books by title, author, keyword or topic.
    """

    url = "https://www.googleapis.com/books/v1/volumes"

    params = {
        "q": query,
        "maxResults": 5,
        "key": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if "items" not in data:
            return "No books found."

        books = []

        for item in data["items"]:

            info = item["volumeInfo"]

            title = info.get("title", "Unknown")

            authors = ", ".join(
                info.get("authors", ["Unknown"])
            )

            publisher = info.get("publisher", "Unknown")

            published = info.get("publishedDate", "Unknown")

            books.append(
                f"""📚 {title}

Author : {authors}
Publisher : {publisher}
Published : {published}
"""
            )

        return "\n-----------------------------\n".join(books)

    except Exception as e:
        return f"Error: {e}"