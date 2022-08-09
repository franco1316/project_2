from rest_framework import serializers
from ..models import *
from .library_user import LibraryUserSerializer, UserSerializer

#do a category as no required field or change the model and the full_db/book
fields_book = [ 'title', 'author', 'category', 'shelf_number', 'price' ]

include_fields_book = [ 'owner', ]
extended_fields_book = [ 'id' ] + fields_book + [ 'date_publication', 'uuid' ] + include_fields_book

class BookSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = (fields_book)
        depth = 1

    def get_price(self, obj):
        try:
            return obj.sprice
        except AttributeError:
            return obj['price']
        

class ExtendedBookSerializer(serializers.ModelSerializer):

    owner = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (extended_fields_book)
        include = (include_fields_book)
        depth = 1
    
    def get_owner(self, obj):
        owners = LibraryUser.objects.all()
        my_owners = {}
        for owner in owners:
            if owner.email != '':
                try:
                    #the following line is the main reason that I made a try except
                    # owner = LibraryUserSerializer(obj.owner, many=False).data 
                    #if by some reason the owner was the user instead some library user
                    owner = LibraryUserSerializer(owner, many=False).data
                except AttributeError:
                    owner = UserSerializer(owner, many=False).data
                my_owners = owner
        if my_owners == {}:
            my_owners == {None}
        return my_owners

    def get_price(self, obj):
        try:
            return obj.sprice
        except AttributeError:
            return obj['price']
        
