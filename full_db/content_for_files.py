from random import randint
from types import FunctionType
import math
import sys
import os
import django

class Config(): 
    def __init__(self, path: str = '../project_2', project: str = 'system') -> None:
        self.relative_path = path
        self.project_name = project

    def config_full_db(self) -> None:
        sys.path.append(self.relative_path)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{self.project_name}.settings")
        django.setup()

#* its was usefull have all as public, literally all
my_config = Config().config_full_db()

#create n rows for each model (Im no recommend bigger values than 1000)
n = 100

wish_delete = False
wish_sof_delete = False
wish_reactive = False

class Dictionary():
    def __init__(self) -> None:
        self.DICTIONARY_ALL_SYMBOLS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890|!"#$%&/()=¿?¨´*+-/[]}{_-:.;,<>\''
        self.DICTIONARY_ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        self.DICTIONARY_NUMBERS = '1234567890'
        self.DICTIONARY_VOCALS = 'aeiouAEIOU'
        self.DICTIONARY_CONSONANTS = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        self.DICTIONARY_SYMBOLS = '|!"#$%&/()=¿?¨´*+-/[]}{_-:.;,<>\''

dict = Dictionary()

def create_charfield(my_function: FunctionType, min_value: int, max_value: int) -> str:
    # len_name = randint(min_value, max_value)
    # name = my_function()
    # name = name[0:len_name]
    # return name
    return my_function()[0:randint(min_value, max_value)]

def charfield_one_word() -> str:
    word = ''
    for i in range(100):
        random_bool = randint(0, 1)
        random_number_for_vocals = randint(0, len(dict.DICTIONARY_VOCALS) - 1)
        random_number_for_consonants = randint(0, len(dict.DICTIONARY_CONSONANTS) - 1)
        consonant = dict.DICTIONARY_CONSONANTS[random_number_for_consonants]
        vocal = dict.DICTIONARY_VOCALS[random_number_for_vocals]
        if random_bool == 0:
            word += consonant + vocal
        else:
            word += vocal + consonant
    return word

def charfield_some_words() -> str:
    words = ''
    for i in range(100):
        random_bool = randint(0, 1)
        number_spaces = randint(1, 15)
        random_number_for_vocals = randint(0, len(dict.DICTIONARY_VOCALS) - 1)
        random_number_for_consonants = randint(0, len(dict.DICTIONARY_CONSONANTS) - 1)
        consonant = dict.DICTIONARY_CONSONANTS[random_number_for_consonants]
        vocal = dict.DICTIONARY_VOCALS[random_number_for_vocals]
        if random_bool == 0:
            words += consonant + vocal
        else:
            words += vocal + consonant
        if i % number_spaces == 3:
            words += ' '
    return words

def charfield_all_symbols() -> str:
    text = ''
    for i in range(100):
        random_number_for_all_symbols = randint(0, len(dict.DICTIONARY_ALL_SYMBOLS) - (len(dict.DICTIONARY_SYMBOLS) + 1))
        text += dict.DICTIONARY_ALL_SYMBOLS[random_number_for_all_symbols]
    return text

def create_decimalfield(len_decimals: int, min_value: float, max_value: float):
    min_int = math.trunc(min_value)
    max_int = math.trunc(max_value)
    digits = randint(min_int, max_int)
    decimals = 0
    for i in range(len_decimals):
        decimals += randint(0, 9) * math.pow(10, -i - 1)
    number = float(digits + decimals)
    
    return number

