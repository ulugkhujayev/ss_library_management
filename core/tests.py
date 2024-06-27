from django.test import TestCase
from django.urls import reverse
from .models import Book, User, Loan


class ViewsTestCase(TestCase):
    def setUp(self):
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

    def test_book_list_view(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_user_list_view(self):
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

    def test_loan_list_view(self):
        book = Book.objects.first()
        user = User.objects.first()
        Loan.objects.create(book=book, user=user)
        response = self.client.get(reverse("loan_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertContains(response, "Test User")

    def test_book_create_view(self):
        response = self.client.post(
            reverse("book_add"),
            {
                "title": "New Book",
                "author": "New Author",
                "publication_year": 2022,
                "genre": "Non-Fiction",
                "status": "available",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_user_create_view(self):
        response = self.client.post(
            reverse("user_add"),
            {"name": "New User", "contact_info": "newuser@example.com"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(name="New User").exists())

    def test_loan_create_view(self):
        book = Book.objects.first()
        user = User.objects.first()
        response = self.client.post(
            reverse("loan_add"),
            {"book": book.id, "user": user.id, "loan_date": "2023-01-01"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Loan.objects.filter(book=book, user=user).exists())

    def test_return_book_view(self):
        book = Book.objects.first()
        user = User.objects.first()
        loan = Loan.objects.create(book=book, user=user)
        response = self.client.get(reverse("return_book", args=[loan.id]))
        self.assertEqual(response.status_code, 302)
        loan.refresh_from_db()
        self.assertIsNotNone(loan.return_date)
        book.refresh_from_db()
        self.assertEqual(book.status, "available")
