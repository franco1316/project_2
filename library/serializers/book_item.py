from rest_framework import serializers
from ..models import *
from .library_user import LibraryUserSerializer
from .book import BookSerializer

fields_book_item = [ 'title', 'quantity', 'shelf_number', 'book' ]

class BookItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField('get_book')
    class Meta:
        model = BookItem
        fields = (fields_book_item)
        depth = 1

    def get_book(self, obj):
        return obj.title


class ExtendedBookItemSerializer(serializers.ModelSerializer):

    my_readers = serializers.SerializerMethodField()
    book = serializers.SerializerMethodField('get_book')
    class Meta:
        model = BookItem
        fields = '__all__'
        depth = 1

    def get_book(self, obj):
        return {
            'title': obj.book.title,
            'category': obj.book.category
        }

    def get_my_readers(self, obj):
        try:
            return obj.owners.fullname
        except AttributeError:
            return None
class CreateBookItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookItem
        fields = '__all__'


