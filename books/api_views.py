from rest_framework import generics, viewsets
from rest_framework.decorators import action

from books.permissions import IsAdminOrReadOnly
from books.serializers import *
from books.models import Book, Genre, SubGenre, Author


class BookAPIViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        subgenre = self.request.query_params.get('subgenre')
        genre = self.request.query_params.get('genre')
        author = self.request.query_params.get('author')
        if subgenre:
            if author:
                return Book.objects.filter(subgenre=subgenre, author=author)
            return Book.objects.filter(subgenre=subgenre)
        elif genre:
            if author:
                return Book.objects.filter(subgenre__genre=genre, author=author)
            return Book.objects.filter(subgenre__genre=genre)
        elif author:
            return Book.objects.filter(author=author)
        return Book.objects.all()


class GenreAPIViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )


class SubGenreAPIViewSet(viewsets.ModelViewSet):
    queryset = SubGenre.objects.all()
    serializer_class = SubGenreSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        genre = self.request.query_params.get('genre')
        if genre:
            return SubGenre.objects.filter(genre=genre)
        return SubGenre.objects.all()


class AuthorAPIViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrReadOnly, )



# class BookAPIView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#
# class BookAPIUpdateView(generics.UpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#
# class BookAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

