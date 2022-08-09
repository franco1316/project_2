from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from library.models import Book
from library.serializers.book import ExtendedBookSerializer, BookSerializer

class BookListApiView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    e_serializer_class = ExtendedBookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'author', 'category', 'date_publication', 'owner__first_name', 'owner__last_name']
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_e_serializer_class(self):
        return self.e_serializer_class

    @action(detail=False, methods=['get'], url_name='info', url_path='info', name='Info')
    def show_info(self, req):
        queryset = self.get_queryset()
        filter_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_queryset)
        if page is not None:
            serializer = self.get_serializer_class()
            data = serializer(page, many=True).data
            return Response({'Books': data}, status=status.HTTP_200_OK)

        serializer = self.get_e_serializer_class()
        data = serializer(filter_queryset, many=True).data

    @action(detail=False, methods=['get'], url_name='more-info', url_path='more-info', name='More info')
    def show_more(self, req):
        queryset = self.get_queryset()
        filter_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_queryset)
        if page is not None:
            serializer = self.get_e_serializer_class()
            data = serializer(page, many=True).data
            return Response({'Books': data}, status=status.HTTP_200_OK)

        serializer = self.get_e_serializer_class()
        data = serializer(filter_queryset, many=True).data

    def __get_slug(self, pk: str):
            if pk.find(':') != -1:
                slug = pk.replace('"', '')
                slug = slug.replace(': ', '=')
                #if the slug come in json format, I delete the format
                slug = slug.split('=')
                slug[0] = slug[0].replace(' ', '')
            else:
                slug = pk.split('=')
            return slug
        
    def __get_book(self, slug):
        pk = slug[1]
        if slug[0] == 'id':
            books = Book.objects.filter(id = pk)
        elif slug[0] == 'title':
            books = Book.objects.filter(title = pk)
        elif slug[0] == 'author':
            books = Book.objects.filter(author = pk)
        elif slug[0] == 'category':
            books = Book.objects.all() 
            my_books = []
            for book in books:
                if book.category == pk:
                    my_books.append(book)
            books = my_books
        elif slug[0] == 'date_publication':
            books = Book.objects.filter(date_publication = pk)
        elif slug[0] == 'subject' or slug[0] == 'owner':
            books = Book.objects.all()
            books = ExtendedBookSerializer(books, many=True).data
            my_books = []
            for book in books:
                owners = book['owner']
                if owners['full_name'] == pk:
                    my_books.append(book)
            books = my_books

        return books

    @action(detail=True, methods=['get'], url_name='info', url_path='info', name='Info')
    def show_one_info(self, req, pk: str=None):
        slug = self.__get_slug(pk = pk)
        book = self.__get_book(slug = slug)
        serializer = self.get_serializer_class()
        data = serializer(book, many=True).data
        response = {"Book": data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='more-info', url_path='more-info', name='More info')
    def show_one_more(self, req, pk:str=None):
        slug = self.__get_slug(pk = pk)
        book = self.__get_book(slug = slug)
        serializer = self.get_e_serializer_class()
        data = serializer(book, many=True).data
        response = {"Book": data}
        return Response(response, status=status.HTTP_200_OK)

