from django.urls import path
from .views import BookDetailView, BookListCreateView, StatsView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-create-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='books-detail'),
    path('stats/', StatsView.as_view(), name='books-stats')
]