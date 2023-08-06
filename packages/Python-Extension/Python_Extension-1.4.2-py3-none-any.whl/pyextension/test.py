import sys

from __init__ import *
if sys.version_info[0] == 3 and sys.version_info[1] >= 10:
    import mathematics as m
from password import *
if sys.version_info[0] == 3 and sys.version_info[1] >= 10:
    import word as w
from word_bank import *
import os

def _clear():
    try:
        for root, dirs, files in os.walk('__pycache__', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir('__pycache__')
    except OSError:
        pass
    try:
        for root, dirs, files in os.walk('word_bank/__pycache__', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir('word_bank/__pycache__')
    except OSError:
        pass
    try:
        os.remove('word bank.dat')
    except OSError:
        pass
    return True

def _test_pyextension():
    computer
    computer()
    python
    python()
    opensource('pyextension')
    opensource('mathematics')
    opensource('password')
    opensource('word bank')
    opensource('word bank data')
    opensource('word')
    message()
    description()
    license()
    word_bank()
    _clear()
    return True

def _test_math():
    if sys.version_info[0] == 3 and sys.version_info[1] >= 10:
        floatdd(1.23)
        m.fibo(5)
        m.fibo(found=5)
        m.fibo(to=5)
        m.arithmetic_sequence('all', '12345')
        return True
    else:
        return 'Mathematics module needs Python 3.10 or more later'

def _test_password():
    decrypt1(encrypt1('abc', 'abcdefg')[0], encrypt1('abc', 'abcdefg')[1])
    decrypt2(encrypt2('abc', 'abcdefg', 5)[0], encrypt2('abc', 'abcdefg', 5)[1])
    decrypt3(encrypt3('abc', 'abcdefg', 'sky')[0], encrypt3('abc', 'abcdefg', 'sky')[1])
    _clear()
    return True

def _test_wordbank():
    a = Word()
    a.search('a')
    a.get()
    _clear()
    try:
        os.remove('word bank.dat')
    except OSError:
        pass
    return True

def _test_word():
    w.add_text('abc')
    w.add_heading('abc')
    _clear()
    return True

def _test(module='all'):
    if module == 'all':
        return (
            _test_pyextension(),
            _test_math(),
            _test_password(),
            _test_wordbank(),
            _test_word()
            )
    elif module == 'pyextension':
        return _test_pyextension()
    elif module == 'math':
        return _test_math()
    elif module == 'password':
        return _test_password()
    elif module == 'word bank' or module == 'word_bank':
        return _test_wordbank()
    elif module == 'word':
        return _test_word()

_clear()
_test()
