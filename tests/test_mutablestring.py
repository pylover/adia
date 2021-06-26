import pytest

from dial.mutablestring import MutableString


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


def test_mutablestring_get():
    s = MutableString('123456')
    assert s[:] == '123456'
    assert s[1:] == '23456'
    assert s[1:4] == '234'
    assert s[:4] == '1234'
    assert s[-2:] == '56'
    assert s[1::2] == '246'


def test_mutablestring_init():
    s = MutableString(5)
    assert s.length == 5
    assert str(s) == '     '


def test_mutablestring_set():
    s = MutableString(5)
    s[1:] = 'foo'
    assert str(s) == ' foo '

    with pytest.raises(ValueError) as e:
        s[1:4] = 'fo'

    assert str(e.value) == \
        'attempt to assign sequence of size 2 to replace with slice of size 3'
