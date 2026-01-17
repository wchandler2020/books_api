Book Catalog API
This API is built user Django and Django REST Framework and an in‑memory storage (a Python dict) for data persistence.

Requirements
Python 3.x

pip

It is recommended to use a virtual environment.

Setup
1. Clone the repository
bash
git clone 
cd <your-repo-folder>
2. Create and activate a virtual environment
bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
3. Install dependencies
If requirements.txt exists:

bash
pip install -r requirements.txt
Otherwise:

bash
pip install django djangorestframework pytest pytest-django
4. Apply migrations
Even though the API uses an in‑memory data store, Django requires base migrations:

bash
python manage.py migrate
Running the API
Start the development server:

bash
python manage.py runserver
By default, the API will be available at:

Base URL: http://127.0.0.1:8000/

API Endpoints
All data is stored in memory for the lifetime of the server process.

1. Create / List books
Endpoint

POST /books/

GET /books/

POST /books/

Create a new book.

Request body (JSON)

json
{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "year": 1937,
  "tags": ["fantasy", "classic"]
}
Constraints:

title: string, required

author: string, required

year: integer, required, 1400 <= year <= current year

tags: optional list of strings

Response (201 Created)

json
{
  "id": 1,
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "year": 1937,
  "tags": ["fantasy", "classic"]
}
If validation fails, a 400 response with error details is returned.

GET /books/

Return a paginated list of books with optional filtering and search.

Query parameters

author – filter by author

year – filter by publication year (integer)

search – case‑insensitive search on title

page – page number (default: 1)

page_size – items per page (default: 10)

Example

bash
GET /books/?author=J.R.R.%20Tolkien&year=1937&search=hobbit&page=1&page_size=10
Response (200 OK)

json
{
  "results": [
    {
      "id": 1,
      "title": "The Hobbit",
      "author": "J.R.R. Tolkien",
      "year": 1937,
      "tags": ["fantasy", "classic"]
    }
  ],
  "count": 1,
  "page": 1,
  "page_size": 10
}
If year cannot be parsed as an integer, a 400 response is returned with an appropriate error message.

2. Retrieve a single book
Endpoint

GET /books/{id}/

Example

bash
GET /books/1/
Response (200 OK)

json
{
  "id": 1,
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "year": 1937,
  "tags": ["fantasy", "classic"]
}
If the book does not exist, a 404 response is returned.

3. Delete a book
Endpoint

DELETE /books/{id}/

Example

bash
DELETE /books/1/
Response

204 No Content or 200 OK (depending on your chosen implementation) if the book is deleted.

404 Not Found if the book does not exist.

4. Catalog stats
Endpoint

GET /stats/

Returns:

Total number of books

Count of unique authors

Example

bash
GET /stats/
Response (200 OK)

json
{
  "total_books": 3,
  "unique_authors": 2
}
Running Tests
Tests cover the main endpoints, validation behavior, and error handling.

With pytest
From the project root:

bash
pytest
With Django’s test runner (optional)
bash
python manage.py test
Design choices
Framework: Django REST Framework for its mature ecosystem, explicit class‑based views, and strong support for serialization and validation.

Storage: In‑memory dict (BOOKS) to avoid database setup, as specified by the challenge.

Type safety: Python type hints for views, helper structures (Book dataclass), and serializers.

Validation: Year range and required fields enforced at the serializer level; invalid query params (like non‑integer year) produce meaningful 400 responses.

Testing: Standard Python testing stack (pytest + pytest-django or Django’s test runner) for easy execution via a single command.

You can adjust wording and details (e.g., ids, status codes) to exactly match your final implementation.
