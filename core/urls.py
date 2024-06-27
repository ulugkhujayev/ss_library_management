from django.urls import path
from .views import (
    BookListView,
    BookCreateView,
    BookUpdateView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    LoanListView,
    LoanCreateView,
    return_book,
)

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("books/add/", BookCreateView.as_view(), name="book_add"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book_edit"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/add/", UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
    path("loans/", LoanListView.as_view(), name="loan_list"),
    path("loans/add/", LoanCreateView.as_view(), name="loan_add"),
    path("loans/<int:pk>/return/", return_book, name="return_book"),
]
