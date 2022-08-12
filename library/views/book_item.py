from urllib import response
from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from library.models import BookItem, Book, LibraryUser
from library.serializers.book_item import CreateBookItemSerializer, ExtendedBookItemSerializer, BookItemSerializer
import json

from ..serializers.library_user import CreateLibraryUserSerializer

class BookItemListApiView(viewsets.ModelViewSet):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer
    create_serializer_class = CreateBookItemSerializer
    extended_serializer_class = ExtendedBookItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'owners', 'book', 'shelf_number', 'rent_by', 'reservation_by']
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    ordering_fields = '__all__'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']

    def get_create_serializer_class(self):
        return self.create_serializer_class

    def get_extended_serializer_class(self):
        return self.extended_serializer_class

    def list(self, req):
        return Response({
            'Info': 'http://127.0.0.1:8000/api/v1/book-items/info',
            'More info': 'http://127.0.0.1:8000/api/v1/book-items/more-info',
            'Add-book-item': 'http://127.0.0.1:8000/api/v1/books/add'
        })

    def create(self, req):
        if req.method == 'GET':
            return Response()
        serializer = self.get_serializer(data=req.data, partial=False)
        serializer.is_valid(raise_exception=True)
        data = req.data
        try:
            title = data['title']
        except:
            return response('The field title is required to realize a post action', status=status.HTTP_206_PARTIAL_CONTENT)
        book = Book.objects.get(title = title)
        new_user = BookItem.objects.create(
            book = book,
            title = title,
            quantity = data.get('quantity', 1),
            rent_by = data.get('rent_by', None),
            reservation_by = data.get('reservation_by', None),
        )
        new_user.save()
        quantity = data.get('quantity', 1)
        return Response({f'New book-item': f'({quantity}) {title}'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'post'], url_name='new-book', url_path='add', name='Book-item For Library')
    def create_book(self, req):
        if req.method == 'GET':
            return Response()
        serializer = self.get_serializer(data=req.data, partial=False)
        serializer.is_valid(raise_exception=True)
        data = req.data
        try:
            title = data['title']
        except:
            return response('The field title is required to realize a post action', status=status.HTTP_206_PARTIAL_CONTENT)
        book = Book.objects.get(title = title)
        new_user = BookItem.objects.create(
            book = book,
            title = title,
            quantity = data.get('quantity', 1),
            rent_by = data.get('rent_by', None),
            reservation_by = data.get('reservation_by', None),
        )
        new_user.save()
        quantity = data.get('quantity', 1)
        return Response({f'New book-item': f'({quantity}) {title}'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'post'], url_name='info', url_path='info', name='Info')
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
        response = (data)
        return Response(response, status=status.HTTP_200_OK)

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
            return Response({'No users'}, status=status.HTTP_204_NO_CONTENT)
        response = (data)
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if self.request.user['role'].find('member') != -1:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            if request.data["owner"]:
                books_items = BookItem.objects.filter(owner=request.data["owner"])
                total = 0
                for book_item in books_items:
                    total += 1
                if total >= 5:
                    return Response('You can\'t have more than 5 books at the same time', status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            if instance['quantity'] > 0:
                data = {
                    "rent_by": request.data.get('owner', None),
                    "reservation_by": request.data["owner"],
                    "quantity": instance['quantity'] - 1
                }
                if data['rent_by'] != None:
                    data['quantity'] = instance[data]
                serializer = self.get_serializer(instance, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)

    @action(detail=True, methods=['get'], url_name='info', url_path='info', name='Info')
    def show_by_id(self, req, pk=None):
        user = BookItem.objects.filter(id = pk)
        serializer = self.get_serializer_class()
        data = serializer(user, many=True).data
        response = (data)
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='more-info', url_path='more-info', name='More info')
    def show_more_by_id(self, req, pk=None):
        user = BookItem.objects.filter(id = pk)
        serializer = self.get_e_serializer_class()
        data = serializer(user, many=True).data
        response = (data)
        return Response(response, status=status.HTTP_200_OK)