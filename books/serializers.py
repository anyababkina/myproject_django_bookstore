from rest_framework import serializers

from books.models import Book, Genre, SubGenre, Author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'description', 'subgenre', 'price', 'amount')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class SubGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubGenre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'