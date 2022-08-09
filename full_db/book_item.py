from content_for_files import (
    my_config, 
    n, wish_delete, wish_sof_delete, wish_reactive,
    create_charfield,
    charfield_some_words as csw
)

from library.models import BookItem, Book
from random import randint

def asign_book() -> object:
    books = Book.objects.all()
    n = randint(0, len(books) - 1)
    book = books[n]
    return book

def create_book_items() -> None:
    for i in range(n):
        quantity = randint(0, 100)
        book = asign_book()
        title = create_charfield(csw, 7, 50).title()
        new_book_item = BookItem.objects.create(
            quantity = quantity,
            book = book,
            title = title
        )
        new_book_item.save()

def data():
    book_items = BookItem.objects.all()
    if len(book_items) > 0:
        if wish_delete:
            book_items.delete()
            print('All copies were burn')
        if wish_sof_delete:
            for book_item in book_items:
                if book_item.quantity > 0:
                    book_item.quantity = 0
            print('All active users are inactive now')
        if wish_reactive:
            for book_item in book_items:
                if book_item.quantity <= 0:
                    book_item.quantity = 1
            print('All inactive users are active now')
    else:
        print('Could not be found any book item')
    if n > 0:
         create_book_items()
         print('Were created {0} book items'.format(n))

    new_quantity = len(BookItem.objects.all())
    print(f'Book items are: {new_quantity}')

data()