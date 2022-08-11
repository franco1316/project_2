from content_for_files import (
    my_config,
    n, wish_delete, wish_sof_delete, wish_reactive,
    create_charfield,
    charfield_one_word as cow,
    charfield_all_symbols as cas
)
from library.models import LibraryUser
from random import randint

roles = [ 'Member', 'Librarian', 'System' ]
def select_role() -> str:
    # choose_one = randint(0, len(roles) - 1)
    # role = roles[choose_one]
    # return role
    return roles[randint(0, len(roles) - 1)]

def create_users() -> None:
    for i in range(n):
        password = create_charfield(cas, 8, 16)
        first_name = create_charfield(cow, 6, 40).title()
        last_name = create_charfield(cow, 3, 20).title()
        fullname = create_charfield(cow, 6, 40).title()
        email_name = f'{first_name[0:-1:3].lower() + last_name[::-3].lower()}'
        email_host = f'{create_charfield(cow, 5, 10).lower()}'
        email = f'{email_name}@{email_host}.com'
        username = create_charfield(cas, 5, 25)
        role = select_role()

        new_library_user = LibraryUser.objects.create(
            username = username,
            password = password,
            fullname = fullname,
            email = email,
            role = role
        )
        new_library_user.save()

def data():
    users = LibraryUser.objects.all()
    if len(users) > 0:
        if wish_delete:
            users.delete()
            print('All library_users were deleted')
        if wish_sof_delete:
            users.filter(is_active = True).update(is_active = False)
            print('All active library_users are inactive now')
        if wish_reactive:
            users.filter(is_active = False).update(is_active = True)
            print('All inactive library_users are active now')
    else:
        print('Could not be found any library_user')
    if n > 0:
        create_users()
        print('Were created {0} library_users'.format(n))

    new_quantity = len(LibraryUser.objects.all())
    print(f'Library users are: {new_quantity}')


data()