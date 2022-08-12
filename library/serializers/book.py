from rest_framework import serializers
from ..models import *
from .library_user import LibraryUserSerializer

#do a category as no required field or change the model and the full_db/book
fields_book = [ 'title', 'author', 'category', 'shelf_number', 'price', 'owner']
extended_fields_book = [ 'id' ] + fields_book + [ 'date_publication', 'uuid' ]

class BookSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = (fields_book)
        depth = 1

    def get_owner(self, obj):
        try:
            return obj.owner.fullname
        except AttributeError:
            return None

    def get_price(self, obj):
        try:
            return obj.sprice
        except AttributeError:
            return obj['price']


class ExtendedBookSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = (extended_fields_book)
        depth = 1

    def get_owner(self, obj):
        try:
            owner = obj.owner
            id = owner.id
            uuid = owner.uuid
            fullname = owner.fullname
            email = owner.email
            password = owner.password
            role = owner.role
            superuser = owner.is_superuser
            status = owner.status
        except AttributeError:
            return None

        if status:
            status = 'active'
        else:
            status = 'inactive'

        if superuser:
            status = f'{status} superuser'
        else:
            status = f'{status} user'

        owner = {
            'id': id,
            'uuid': uuid,
            'fullname': fullname,
            'email': email,
            'password': password,
            'role': role,
            'status': status,
        }

        return owner

    def get_price(self, obj):
        try:
            return obj.sprice
        except AttributeError:
            return obj['price']

class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'