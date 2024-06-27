from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from .models import Book, User, Loan
from .forms import BookForm, UserForm, LoanForm


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        status = self.request.GET.get("status")
        if status:
            return Book.objects.filter(status=status)
        return Book.objects.all()


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "book_form.html"
    success_url = "/books/"


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "book_form.html"
    success_url = "/books/"


class UserListView(ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "user_form.html"
    success_url = "/users/"


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "user_form.html"
    success_url = "/users/"


class LoanListView(ListView):
    model = Loan
    template_name = "loan_list.html"
    context_object_name = "loans"


class LoanCreateView(CreateView):
    model = Loan
    form_class = LoanForm
    template_name = "loan_form.html"
    success_url = "/loans/"

    def form_valid(self, form):
        loan = form.save(commit=False)
        book = loan.book
        book.status = "borrowed"
        book.save()
        return super().form_valid(form)


def return_book(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    loan.return_date = timezone.now()
    loan.save()
    loan.book.status = "available"
    loan.book.save()
    return redirect("loan_list")
