from rest_framework import serializers
from ..models import LibraryUser


include_fields_library_user = [ 'full_name', 'status' ]
fields_library_user =  include_fields_library_user +[ 'email', 'role' ] 

include_extended_fields_library_user = (include_fields_library_user)
extended_fields_library_user = ([ 'id', 'first_name', 'last_name' ] + fields_library_user)

fields_user = [ 'full_name', 'email' ]
 

class LibraryUserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = LibraryUser
        fields = (fields_library_user)
        include = (include_fields_library_user)

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    def get_status(self, obj):
        issu = obj.is_superuser
        iss = obj.is_staff
        isa = obj.is_active
        return f'is_superuser: {issu}, is_staff: {iss}, is_active: {isa}'


class ExtendedLibraryUserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = LibraryUser
        fields = (extended_fields_library_user)
        include = (include_extended_fields_library_user)

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    def get_status(self, obj):
        issu = obj.is_superuser
        iss = obj.is_staff
        isa = obj.is_active
        return f'is_superuser: {issu}, is_staff: {iss}, is_active: {isa}'


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = LibraryUser
        fields = (fields_user)
        include = (include_fields_library_user)

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

"""
    In this app maybe we have the case for some unconsidered reason that the owner of some book be a user without a role
    beacuse the role is a field of library user but this field doesn't exist for the users
"""