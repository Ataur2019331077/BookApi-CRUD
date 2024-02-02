from django.urls import path

from .views import AddBook, UpdateBook, GetBook, SearchBook

urlpatterns = [
    path("books", AddBook.as_view(), name="add-book"),
    #path("books", GetBooks.as_view(), name="get-books"),
    path("books/search", SearchBook.as_view(), name="search-book"),
    path("books/<int:id>", GetBook.as_view(), name="get-book"),
    path("books/<int:id>", UpdateBook.as_view(), name="update-book"),
]