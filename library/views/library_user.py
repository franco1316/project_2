from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from library.models import LibraryUser
from library.serializers.library_user import LibraryUserSerializer, CreateLibraryUserSerializer, ExtendedLibraryUserSerializer

class LibraryUserListApiView(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer
    create_serializer_class = CreateLibraryUserSerializer
    extended_serializer_class = ExtendedLibraryUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'fullname', 'email', 'username']
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_create_serializer_class(self):
        return self.create_serializer_class

    def get_extended_serializer_class(self):
        return self.extended_serializer_class

    def list(self, req):
        return Response({
            'Info': 'http://127.0.0.1:8000/api/v1/users/info',
            'More info': 'http://127.0.0.1:8000/api/v1/users/more-info'
        })

    def create(self, req):
        serializer = self.get_create_serializer_class()
        data = serializer(req.POST, many=False).data
        new_user = LibraryUser.objects.create(data)
        new_user.save()
        return Response({f'New user': data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_name='info', url_path='info', name='Info')
    def show_info(self, req):
        queryset = self.get_queryset()
        filter_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_queryset)
        if page is None:
            return Response({'Error'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer_class()
        data = serializer(page, many=True).data
        if len(data) == 0:
            return Response({'No data'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'Users': data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='more-info', url_path='more-info', name='More info')
    def show_more(self, req):
        queryset = self.get_queryset()
        filter_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_queryset)
        if page is None:
            return Response({'Error'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_extended_serializer_class()
        data = serializer(page, many=True).data
        if len(data) == 0:
            return Response({'No data'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'Users': data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='info', url_path='info', name='Info')
    def show_by_id(self, req, pk=None):
        users = self.get_queryset()
        user = users.filter(id = pk)
        serializer = self.get_serializer_class()
        data = serializer(user, many=True).data
        username = data[0]['full_name']
        response = {"User {0}".format(username): data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='more-info', url_path='more-info', name='More info')
    def show_more_by_id(self, req, pk=None):
        users = self.get_queryset()
        user = users.filter(id = pk)
        serializer = self.get_e_serializer_class()
        data = serializer(user, many=True).data
        username = data[0]['full_name']
        response = {"User {0}".format(username): data}
        return Response(response, status=status.HTTP_200_OK)
