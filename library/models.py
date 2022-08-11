from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50, default='My amazing title', blank=False)
    author = models.CharField(max_length=70, default='Authors', blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=60, blank=False)
    date_publication = models.DateField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True)
    shelf_number = models.CharField(max_length=2, editable=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    is_here = models.BooleanField(default=True, blank=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = self.title.title()
        self.author = self.author.title()
        self.category = self.category.capitalize()
        self.shelf_number = f'{self.title[0]}{self.id}'
        self.sprice = f"${self.price}"

    def __str__(self) -> str:
        title = self.title.capitalize()
        author = self.author.title()
        owner = str(self.owner).title()
        category = self.category.lower()
        price = self.sprice
        return f'Title: {title} | Authors: {author} | Category: {category} | Owner: {owner} | Price: {price}'

class LibraryUser(models.Model):

    choices = [
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
        ('System', 'System'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, blank=False, editable=False, unique=True)
    fullname = models.CharField(max_length=150, blank=False)
    username = models.CharField(max_length=30, blank=True, unique=True)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=False)
    password = models.CharField(max_length=50, blank=True, null=False)
    role = models.CharField(max_length=15, choices=choices)
    is_superuser = models.BooleanField(default=False)
    status = models.BooleanField(default=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable= False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fullname = self.fullname.title()

    def __str__(self) -> str:
        return self.fullname

class BookItem(models.Model):
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book', blank=True, null=True)
    owners = models.ManyToManyField(User, blank=True)
    title = models.CharField(max_length=50, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    shelf_number = models.CharField(max_length=2, editable=False)
    rent_by = models.OneToOneField(LibraryUser, on_delete=models.CASCADE, related_name='rent', null=True, blank=True)
    reservation_by = models.OneToOneField(LibraryUser, on_delete=models.CASCADE, related_name='reservation', null=True, blank=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = self.title.title()
        current_book = self.book
        if current_book != None:
            self.title = current_book.title.title()
            self.uuid = current_book.uuid
            self.shelf_number = current_book.shelf_number


    def __str__(self) -> str:
        users = ''
        for i, user in enumerate(self.owners.all()):
            if i < len(self.owners.all()) -1:
                users = f'{users}{user}, '
            elif i == len(self.owners.all()) -1:
                users = f'{users}{user}'
        users = users.title()
        title = f'{self.book}'.split('|')[0].title()
        author = f'{self.book}'.split('|')[1].title()
        quantity = self.quantity
        if len(users) > 0:
            return f'({quantity}) [{title} | {author}] => {users}'
        else:
            return f'({quantity}) [{title} | {author}]'
