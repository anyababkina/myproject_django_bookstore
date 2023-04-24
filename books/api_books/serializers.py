from rest_framework import serializers

from books.models import Book, Genre, SubGenre, Author


class BookSerializer(serializers.ModelSerializer):
    subgenre = serializers.StringRelatedField()
    author = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ('title', 'description', 'subgenre', 'price', 'amount', 'author')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class SubGenreSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField()

    class Meta:
        model = SubGenre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'

