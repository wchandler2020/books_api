from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BookSerializer

#will be use as in memory storage.
@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    tags: Optional[List[str]]

BOOKS: Dict[int, Book] = {}

NEXT_ID: int = 1


class BookListCreateView(generics.ListCreateAPIView):
    '''
        This view will list and filter all of
        the and also create a new book
    '''

    serializer_class = BookSerializer

    def get_queryset(self) -> List[Book]:
        books = list(BOOKS.values())
        #filter by author
        author = self.request.query_params.get("author")

        if author:
            books = [b for b in books if b.author == author]
        #filter by year
        year = self.request.query_params.get("year")
        if year:
            # list() will handle validation; year format errors handled in list()
            try:
                year_int = int(year)
            except ValueError:
                # let list() handle returning the 400
                return books
            books = [b for b in books if b.year == year_int]
        #filter by search param
        search = self.request.query_params.get("search")
        if search:
            lookup = search.lower()
            books = [b for b in books if lookup in b.title.lower()]

        return books

    def list(self, request: Request, *args, **kwargs) -> Response:
        '''this function will override the list to handle validating
        the year and add pagination'''
        year = request.query_params.get("year")
        if year:
            try:
                int(year)
            except ValueError:
                return Response(
                    {"detail": "year must be a number."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))

        queryset = self.get_queryset()
        start = (page - 1) * page_size
        end = start + page_size
        sliced = queryset[start:end]

        serializer = self.get_serializer(sliced, many=True)
        return Response(
            {
                "results": serializer.data,
                "count": len(queryset),
                "page": page,
                "page_size": page_size,
            }
        )

    def create(self, request: Request, *args, **kwargs) -> Response:
        '''this function will override the create, this will
        handle saving the book data to the in memory storage...BOOKS Dict'''
        global NEXT_ID

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        book = Book(
            id=NEXT_ID,
            title=data["title"],
            author=data["author"],
            year=data["year"],
            tags=data.get("tags") or [],
        )

        BOOKS[NEXT_ID] = book
        NEXT_ID += 1

        out_serializer = self.get_serializer(book)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)


class BookDetailView(generics.RetrieveDestroyAPIView):
    '''
        this will allow us to delete or retrieve a book instance,
        this will be out GET and DELETE apiviews
    '''

    serializer_class = BookSerializer
    lookup_field = "pk"

    def get_object(self) -> Book:
        pk = self.kwargs.get("pk")
        book = BOOKS.get(pk)
        if not book:
            raise NotFound()
        return book

    def perform_destroy(self, instance: Book) -> None:
        '''delete/destroy a book object'''
        # instance is the Book returned by get_object()
        # find its key in BOOKS and remove it
        for pk, book in list(BOOKS.items()):
            if book is instance:
                del BOOKS[pk]
                break


class StatsView(APIView):
    '''
        this view will inherit from the APIView,
        generics is a simple way of creating CRUD pattern
        in an API, stets endpoint is not a part of the CRUD operations.
        this view will just return the books stats like page numbers and author
    '''

    def get(self, request: Request) -> Response:
        total_books = len(BOOKS)
        unique_authors = {b.author for b in BOOKS.values()}
        return Response(
            {
                "total_books": total_books,
                "unique_authors": len(unique_authors),
            }
        )
