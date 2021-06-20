from dial.sequence import Call


def test_call():
    assert repr(Call('foo', 'bar')) == 'foo -> bar'
    bar = Call('bar', 'baz', [
        Call('baz', 'quux', [
            Call('quux', 'fred')
        ]),
        Call('baz', 'thud')
    ])

    assert repr(bar) == '''\
bar -> baz:
  baz -> quux:
    quux -> fred
  baz -> thud
'''

    assert bar != Call('bar', 'baz', [
        Call('bad', 'quux', [
            Call('quux', 'fred')
        ]),
        Call('baz', 'thud')
    ])

    assert bar != Call('bar', 'baz', [
        Call('baz', 'thud')
    ])

    assert bar != []
    assert not bar == []
