from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import pytest

@pytest.fixture
def client() -> APIClient:
    return APIClient()

def test_create_book_success(client: APIClient) -> None:
    resp = client.post(
        '/books/',
        {
            'title': 'Test',
            'author': 'Author',
            'year': 2020,
            'tags': ['fiction'],
        },
        format='json'
    )
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert data["id"] > 0
    assert data["title"] == "Test"

def test_create_book_book_validator(client: APIClient) -> None:
    resp = client.post(
        "/books/",
        {
            "title": "Bad",
            "author": "Author",
            "year": 1300,
        },
        format="json",
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "year" in resp.json()

