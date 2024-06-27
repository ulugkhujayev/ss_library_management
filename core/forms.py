from django import forms
from .models import Book, User, Loan


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year", "genre", "status"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "contact_info"]


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["book", "user", "loan_date", "return_date"]

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get("book")
        if book and book.status == "borrowed":
            raise forms.ValidationError("This book is already borrowed.")
        return cleaned_data
