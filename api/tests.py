from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Book, User, Loan
from django.utils import timezone


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_year=2021,
            genre="Fiction",
            status="available",
        )
        self.user = User.objects.create(
            name="Test User", contact_info="test@example.com"
        )

    def test_book_list(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_book_create(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "publication_year": 2022,
            "genre": "Non-Fiction",
            "status": "available",
        }
        response = self.client.post(reverse("book-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_user_list(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_user_create(self):
        data = {"name": "New User", "contact_info": "newuser@example.com"}
        response = self.client.post(reverse("user-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_loan_create(self):
        data = {
            "book": self.book.id,
            "user": self.user.id,
            "loan_date": timezone.now().date().isoformat(),
        }
        response = self.client.post(reverse("loan-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, "borrowed")

    def test_return_book(self):
        loan = Loan.objects.create(book=self.book, user=self.user)
        response = self.client.post(reverse("loan-return-book", args=[loan.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        loan.refresh_from_db()
        self.assertIsNotNone(loan.return_date)
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, "available")
