from dial.mutablestring import MutableString

from .helpers import raises


def test_mutablestring_remove():
    s = MutableString('123')
    s.remove('2')
    assert s == '13'


def test_mutablestring_extend():
    s = MutableString('123')
    s.extend('456')
    assert s == '123456'

    s += '78'
    assert s == '12345678'


def test_mutablestring_reverse():
    s = MutableString('123456')
    s.reverse()
    assert s == '654321'


def test_mutablestring_append():
    s = MutableString('1')
    s.append('2')
    assert s == '12'

    with raises(ValueError) as e:
        s.append('34')
    assert str(e.value) == 'attempt to append multiple characters: 34'

    with raises(ValueError) as e:
        s.append('')
    assert str(e.value) == 'attempt to append zero characters'


def test_mutablestring_pop():
    s = MutableString('123456')
    with raises(ValueError) as e:
        s.pop()

    assert str(e.value) == 'attempt to pop from MutableString of size 6'


def test_mutablestring_insert():
    s = MutableString('123456')
    s.insert(0, 'a')
    assert s == 'a123456'

    s.insert(2, 'b')
    assert s == 'a1b23456'


def test_mutablestring_len():
    s = MutableString('123456')
    assert len(s) == 6


def test_mutablestring_repr():
    s = MutableString('123456')
    assert repr(s) == '\'123456\''


def test_mutablestring_eq():
    s = MutableString('123456')
    assert s == '123456'
    assert not s == 'foo'

    assert s == list('123456')


def test_mutablestring_ne():
    s = MutableString('123456')
    assert s != 'foo'
    assert not (s != '123456')

    assert s != list('foo')


def test_mutablestring_delitem():
    s = MutableString('1a2b3c4d5e6')
    del s[1::2]
    assert s == '123456'

    del s[0]
    assert s == '23456'

    del s[:3]
    assert s == '56'


def test_mutablestring_getitem():
    s = MutableString('123456')
    assert s[:] == '123456'
    assert s[1:] == '23456'
    assert s[1:4] == '234'
    assert s[:4] == '1234'
    assert s[-2:] == '56'
    assert s[1::2] == '246'


def test_mutablestring_setitem():
    s = MutableString(5)
    s[1:] = 'foo'
    assert str(s) == ' foo '

    with raises(ValueError) as e:
        s[1:4] = 'fo'

    assert str(e.value) == \
        'attempt to assign sequence of size 2 to replace with slice of size 3'


def test_mutablestring_init():
    s = MutableString(5)
    assert s.length == 5
    assert str(s) == '     '
