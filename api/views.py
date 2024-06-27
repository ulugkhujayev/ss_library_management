from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Book, User, Loan
from .serializers import (
    BookSerializer,
    UserSerializer,
    LoanSerializer,
    LoanCreateSerializer,
)
from django.utils import timezone


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        status = self.request.query_params.get("status", None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return LoanCreateSerializer
        return LoanSerializer

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.return_date:
            return Response(
                {"error": "This book has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        loan.return_date = timezone.now()
        loan.save()
        loan.book.status = "available"
        loan.book.save()
        return Response(
            {"message": "Book returned successfully."}, status=status.HTTP_200_OK
        )
