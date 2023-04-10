
from django.urls import path, include
from rest_framework import routers

from .api_views import *
from .views import *


rout = routers.SimpleRouter()
rout.register(r'booklist', BookAPIViewSet)
rout.register(r'genre', GenreAPIViewSet)
rout.register(r'subgenre', SubGenreAPIViewSet)
rout.register(r'authorlist', AuthorAPIViewSet)


urlpatterns = [
    path('', home, name='home'),
    path('general_store/', StoreListView.as_view(), name='store'),
    path('contact_us/', contact_us, name='contacts'),
    path('books/<int:book_id>/', AboutBookView.as_view(), name='about_book'),
    path('author/<int:author_id>/', AboutAuthorView.as_view(), name='about_author'),
    path('genres/<int:genre_id>/', GenresListView.as_view(), name='genres'),
    path('subgenres/<int:subgenre_id>/', SubGenresListView.as_view(), name='subgenres'),
    path('searching/', SearchBookListView.as_view(), name='searching'),
    path('api/v1/', include(rout.urls)),
    path('api/v1/user-auth/', include('rest_framework.urls'))
    # path('api/v1/booklist', BookAPIViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('api/v1/booklist/<int:pk>', BookAPIViewSet.as_view({'put': 'update'})),
    # path('api/v1/bookdetail/<int:pk>', BookAPIDetailView.as_view())

]