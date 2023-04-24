from django.urls import path, include
from rest_framework import routers
from books.api_books.api_views import *


rout = routers.SimpleRouter()
rout.register(r'booklist', BookAPIViewSet)
rout.register(r'genre', GenreAPIViewSet)
rout.register(r'subgenre', SubGenreAPIViewSet)
rout.register(r'authorlist', AuthorAPIViewSet)

urlpatterns = [
    path('v1/', include(rout.urls)),
    path('v1/user-auth/', include('rest_framework.urls'))
]