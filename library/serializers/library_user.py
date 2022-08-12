from sqlite3 import IntegrityError
from rest_framework import serializers
from ..models import LibraryUser

exclude_fields_library_user = ['id', 'uuid', 'status', 'is_superuser', 'created_at', 'updated_at']
read_only_fields_library_user = ['id', 'uuid']
#
fields_library_user = [ 'fullname', 'email', 'role' ]

extended_fields_library_user = ([ 'id', 'uuid' ] + fields_library_user + ['status', 'is_superuser'])

class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        exclude = (exclude_fields_library_user)
        read_only = (read_only_fields_library_user)
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ExtendedLibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = (extended_fields_library_user)

class CreateLibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = '__all__'
        read_only_fields = (read_only_fields_library_user)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UpdateLibraryUserSerializer(serializers.ModelSerializer):
    pass
"""
    In this app maybe we have the case for some unconsidered reason that the owner of some book be a user without a role
    beacuse the role is a field of library user but this field doesn't exist for the users
"""