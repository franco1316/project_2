from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from library.models import Book
from library.serializers.book import ExtendedBookSerializer, BookSerializer

class BookListApiView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    e_serializer_class = ExtendedBookSerializer
    http_method_names = ['get', 'head']

    def get_e_serializer_class(self):
        return self.e_serializer_class

    @action(detail=False)
    def show_info(self, req):
        books = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(books, many=True).data
        return Response({"Books": data}, status=status.HTTP_200_OK)

    @action(detail=False)
    def show_more(self, req):
        books = self.get_queryset()
        serializer = self.get_e_serializer_class()
        data = serializer(books, many=True).data
        return Response({"Books": data}, status=status.HTTP_200_OK)

    class BookByListApiView(viewsets.ModelViewSet):
        queryset = Book.objects.all()
        serializer_class = BookSerializer
        e_serializer_class = ExtendedBookSerializer
        http_method_names = ['get', 'head']

        def get_e_serializer_class(self):
            return self.e_serializer_class

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

        @action(detail=True)
        def show_info(self, req, pk: str=None):
            slug = self.__get_slug(pk = pk)
            book = self.__get_book(slug = slug)
            serializer = self.get_serializer_class()
            data = serializer(book, many=True).data
            response = {"Book": data}
            return Response(response, status=status.HTTP_200_OK)

        @action(detail=True)
        def show_more(self, req, pk:str=None):
            slug = self.__get_slug(pk = pk)
            book = self.__get_book(slug = slug)
            serializer = self.get_e_serializer_class()
            data = serializer(book, many=True).data
            response = {"Book": data}
            return Response(response, status=status.HTTP_200_OK)
