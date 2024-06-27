from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[("available", "Available"), ("borrowed", "Borrowed")],
        default="available",
    )

    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.TextField()

    def __str__(self):
        return self.name


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} - {self.user.name}"
