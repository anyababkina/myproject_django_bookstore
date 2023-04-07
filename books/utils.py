from books.models import Book


class DataMixin:
    model = Book
    template_name = 'books/genres.html'
    context_object_name = 'book'
    paginate_by = 5
