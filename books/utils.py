from books.models import Book

options_filter = [('-price', 'убыванию цены'), ('price', 'возрастанию цены'),
                  ('-amount', 'количеству на складе (по убыванию)'), ('amount', 'количеству на складе (по возрастанию')]


class DataMixin:
    model = Book
    template_name = 'books/genres.html'
    context_object_name = 'book'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['option'] = options_filter
        context['sel_value'] = self.request.GET.get('order-by', None)
        return context
