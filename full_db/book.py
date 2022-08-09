from content_for_files import (
    my_config, 
    n, wish_delete, wish_sof_delete, wish_reactive,
    create_charfield,
    charfield_one_word as cow, 
    charfield_some_words as csw,
    create_decimalfield
)
from library.models import Book
        
def create_books() -> None:
    for i in range(n):
        title = create_charfield(csw, 7, 50).title()
        author = create_charfield(csw, 0, 70).title()
        category = create_charfield(cow, 0, 60).capitalize()
        price = create_decimalfield(2, 0.0, 99999.99)

        new_book = Book.objects.create(
            title = title,
            author = author,
            category = category,
            price = price
        )
        new_book.save()

def data():
    books = Book.objects.all()
    if len(books) > 0:
        if wish_delete:
            Book.objects.all().delete()
            print('All books are burned now')
        if wish_sof_delete:
            Book.objects.filter(is_here = True).update(is_here = False)
            print('All books here are gone now')
        if wish_reactive:
            books = Book.objects.filter(is_here = False).update(is_here = True)
            print('All books here are came back')
    else:
        print('Could not be found any book')
    if n > 0:
        create_books()
        print('Were created {0} books'.format(n))

    new_quantity = len(Book.objects.all())
    print(f'Books are: {new_quantity}')

data()
