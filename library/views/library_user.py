from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from library.models import LibraryUser
from library.serializers.library_user import ExtendedLibraryUserSerializer, LibraryUserSerializer

class LibraryUserListApiView(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer
    e_serializer_class = ExtendedLibraryUserSerializer

    def get_e_serializer_class(self):
        return self.e_serializer_class

    def list(self, req):
        message = 'Select an extra action'
        return Response({'message': message}, status=status.HTTP_200_OK)

    def create(self, req):
        pass

    @action(detail=False, methods=['get'])
    def show_info(self, req):
        query_set = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(query_set, many=True).data
        return Response({"Users": data}, status=status.HTTP_200_OK)

    @action(detail=False)
    def show_more(self, req):
        users = self.get_queryset()
        serializer = self.get_e_serializer_class()
        data = serializer(users, many=True).data
        return Response({"Users": data}, status=status.HTTP_200_OK)

    @action(detail=True)
    def show_by_id(self, req, pk=None):
        users = self.get_queryset()
        user = users.filter(id = pk)
        serializer = self.get_serializer_class()
        data = serializer(user, many=True).data
        username = data[0]['full_name']
        response = {"User {0}".format(username): data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True)
    def show_more_by_id(self, req, pk=None):
        users = self.get_queryset()
        user = users.filter(id = pk)
        serializer = self.get_e_serializer_class()
        data = serializer(user, many=True).data
        username = data[0]['full_name']
        response = {"User {0}".format(username): data}
        return Response(response, status=status.HTTP_200_OK)
