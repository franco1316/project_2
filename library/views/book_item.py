from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from library.models import BookItem
from library.serializers.book_item import ExtendedBookItemSerializer, BookItemSerializer

class BookItemListApiView(viewsets.ModelViewSet):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer
    e_serializer_class = ExtendedBookItemSerializer
    http_method_names = ['get', 'head']

    def get_e_serializer_class(self):
        return self.e_serializer_class

    @action(detail=False)
    def show_info(self, req):
        book_items = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(book_items, many=True).data
        return Response({"Book-items": data}, status=status.HTTP_200_OK)

    @action(detail=False)
    def show_more(self, req):
        book_items = self.get_queryset()
        serializer = self.get_e_serializer_class()
        data = serializer(book_items, many=True).data
        return Response({"Book-items": data}, status=status.HTTP_200_OK)

    @action(detail=True)
    def show_by_id(self, req, pk=None):
        user = BookItem.objects.filter(id = pk)
        serializer = self.get_serializer_class()
        data = serializer(user, many=True).data
        response = {"Book-item": data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True)
    def show_more_by_id(self, req, pk=None):
        user = BookItem.objects.filter(id = pk)
        serializer = self.get_e_serializer_class()
        data = serializer(user, many=True).data
        response = {"Book-item": data}
        return Response(response, status=status.HTTP_200_OK)