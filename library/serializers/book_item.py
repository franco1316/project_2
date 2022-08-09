from rest_framework import serializers
from ..models import *
from .library_user import LibraryUserSerializer
from .book import BookSerializer

fields_book_item = [ 'title', 'quantity', 'shelf_number', 'my_book' ]

include_extended_fields_book_item = [ 'my_readers', ]
extended_fields_book_item = [ 'id' ] + fields_book_item + include_extended_fields_book_item + [ 'uuid' ]

class BookItemSerializer(serializers.ModelSerializer):
    my_book = serializers.SerializerMethodField()
    
    class Meta:
        model = BookItem
        fields = (fields_book_item)

    def get_my_book(self, obj):
        book = Book.objects.filter(title = obj.title)
        books = Book.objects.all()
        my_book = {}
        for book in books:
            if book.title != '' or book.author != '':
                if book.title.title() == obj.title.title():
                    my_book = book
        if my_book == {}:
            return 'Don\'t found any book'
        book = BookSerializer(my_book, many = False).data
        return book


class ExtendedBookItemSerializer(serializers.ModelSerializer):

    my_readers = serializers.SerializerMethodField()
    my_book = serializers.SerializerMethodField()
    
    class Meta:
        model = BookItem
        fields = (extended_fields_book_item)
        include = (include_extended_fields_book_item)
        depth = 1

    def get_my_readers(self, obj):
        owners = obj.owners.all()
        my_owners = []
        for owner in owners:
            if owner.email != '':
                my_owners.append(owner)
        return LibraryUserSerializer(my_owners, many = True).data

    def get_my_book(self, obj):
        books = Book.objects.all()
        my_books = {}
        for book in books:
            if book.title != '' or book.author != '':
                if book.title.title() == obj.title.title():
                    my_books = book
        book = BookSerializer(my_books, many = False).data
        return book




        