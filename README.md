## Book Catalog API
This API is built using Django and Django REST Framework and an in‑memory storage (a Python dict) for data persistence.

I choose to use Django for a few reasons: 
1. Familiarity
2. it has a mature ecosystem,
3. class‑based views, and support for serialization and validation, which was important since a database was not being used.

# Requirements
Python 3.x

pip

It is recommended to use a virtual environment.

Setup
1. Clone the repository
bash
git clone https://github.com/wchandler2020/books_api.git
cd your folder

3. Create and activate a virtual environment
4. 
python -m venv venv

# Windows
venv\Scripts\activate

# macOS or Linux
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
All data is stored in memory while the server is running.

1. Create / List books
Endpoint

POST /books/

GET /books/

POST /books/

Create a new book.
You can do this using an API client like Postman or Insomnia

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

To return a list of books with optional filtering and search.

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
Tests cover the main endpoints, validation, and error handling.

# Using pytest
From the project root:

bash
pytest
With Django’s test runner (optional)
bash
python manage.py test




