
from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    path('', cache_page(60 * 5)(home), name='home'),
    path('general_store/', StoreListView.as_view(), name='store'),
    path('contact_us/', cache_page(60 * 5)(contact_us), name='contacts'),
    path('books/<int:book_id>/', cache_page(60 * 5)(AboutBookView.as_view()), name='about_book'),
    path('author/<int:author_id>/', cache_page(60 * 5)(AboutAuthorView.as_view()), name='about_author'),
    path('genres/<int:genre_id>/', GenresListView.as_view(), name='genres'),
    path('subgenres/<int:subgenre_id>/', SubGenresListView.as_view(), name='subgenres'),
    path('searching/', SearchBookListView.as_view(), name='searching'),
]