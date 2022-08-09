import os
from content_for_files import (
    n, wish_delete,
)

#* Don't delete my_config from import in these files, see content_for_files line 20
list_models = ['library_user', 'book', 'book_item']

# Only delete need this order to execute without a recursion error
if wish_delete and n == 0:
    list_models = ['library_user', 'book_item', 'book']
# Delete and create at the same time is completly impossible without have a recursion error
elif wish_delete and n != 0:
    list_models = []
    print('Can\'t realize this action, is impossible delete and create at the same time, please do each one separetly')

# Not try to import nothing of here from any of list models or you create a bucle between the files
# This file is only for execute the others
for model in list_models:
    os.system(f'py full_db/{model}.py')

#* py full_db/execute.py
#* python full_db/execute.py