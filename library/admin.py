from django.contrib import admin
from .models import *

# Register your models here.

my_models = [Book, BookItem, LibraryUser]

for model in my_models:
    admin.site.register(model)
