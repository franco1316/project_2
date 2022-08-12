from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from library.models import Book
from library.serializers.book import CreateBookSerializer, BookSerializer, ExtendedBookSerializer

class BookListApiView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    create_serializer_class = CreateBookSerializer
    extended_serializer_class = ExtendedBookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'author', 'category', 'date_publication']
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    ordering_fields = '__all__'

    def get_create_serializer_class(self):
        return self.create_serializer_class

    def get_extended_serializer_class(self):
        return self.extended_serializer_class

    def list(self, req):
        return Response({
            'Info': 'http://127.0.0.1:8000/api/v1/books/info',
            'More-info': 'http://127.0.0.1:8000/api/v1/books/more-info',
            'Add-book': 'http://127.0.0.1:8000/api/v1/books/add'
        })

    def create(self, req):
        if req.method == 'GET':
            return Response()
        serializer = self.get_serializer(data=req.data, partial=False)
        serializer.is_valid(raise_exception=True)
        data = req.data
        new_user = Book.objects.create(
            title = data['title'],
            author = data['author'],
            category = data['category'],
            price = data['price'],
        )
        new_user.save()
        return Response({f'New book': data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'post'], url_name='new-book', url_path='add', name='Book For Library')
    def create_book(self, req):
        if req.method == 'GET':
            return Response()
        serializer = self.get_serializer(data=req.data, partial=False)
        serializer.is_valid(raise_exception=True)
        data = req.data
        new_user = Book.objects.create(
            title = data['title'],
            author = data['author'],
            category = data['category'],
            price = data['price'],
        )
        new_user.save()
        return Response({f'New book': data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_name='get-info', url_path='info', name='Get Info')
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
            return Response({'No data'}, status=status.HTTP_204_NO_CONTENT)
        response = (data)
        return Response(response, status=status.HTTP_200_OK)

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

    @action(detail=True, methods=['get'], url_name='get-info', url_path='info', name='Get Info')
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


