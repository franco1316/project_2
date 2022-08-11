from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from library.models import BookItem
from library.serializers.book_item import CreateBookItemSerializer, ExtendedBookItemSerializer, BookItemSerializer
import json

class BookItemListApiView(viewsets.ModelViewSet):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer
    create_serializer_class = CreateBookItemSerializer
    extended_serializer_class = ExtendedBookItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'owners', 'book', 'shelf_number', 'rent_by', 'reservation_by']
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_create_serializer_class(self):
        return self.create_serializer_class

    def get_extended_serializer_class(self):
        return self.extended_serializer_class

    def list(self, req):
        return Response({
            'Info': 'http://127.0.0.1:8000/api/v1/book-items/info',
            'More info': 'http://127.0.0.1:8000/api/v1/book-items/more-info'
        })

    def create(self, req):
        return Response('Something')

    @action(detail=False, methods=['get', 'post'], url_name='info', url_path='info', name='Info')
    def show_info(self, req):
        if req.method == 'GET':
            queryset = self.get_queryset()
            filter_queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(filter_queryset)
            if page is None:
                return Response({'Error'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer_class()
            data = serializer(page, many=True).data
            if len(data) == 0:
                return Response({'No data'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'Book items': data}, status=status.HTTP_200_OK)
        elif req.method == 'POST':
            print('Post', req.data)
            serializer = self.get_create_serializer_class()
            data =  serializer(req.data, many=True).data
            return Response({f'Update book item {data.title}':data})

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
        return Response({'Book items': data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='info', url_path='info', name='Info')
    def show_by_id(self, req, pk=None):
        user = BookItem.objects.filter(id = pk)
        serializer = self.get_serializer_class()
        data = serializer(user, many=True).data
        response = {"Book-item": data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='more-info', url_path='more-info', name='More info')
    def show_more_by_id(self, req, pk=None):
        user = BookItem.objects.filter(id = pk)
        serializer = self.get_e_serializer_class()
        data = serializer(user, many=True).data
        response = {"Book-item": data}
        return Response(response, status=status.HTTP_200_OK)