from rest_framework import serializers
from core.models import Book, User, Loan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "publication_year", "genre", "status"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "contact_info"]


class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ["id", "book", "user", "loan_date", "return_date"]


class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "book", "user", "loan_date", "return_date"]

    def create(self, validated_data):
        book = validated_data["book"]
        if book.status == "borrowed":
            raise serializers.ValidationError("This book is already borrowed.")
        book.status = "borrowed"
        book.save()
        return super().create(validated_data)
