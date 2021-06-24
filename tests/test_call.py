from dial.sequence import Call, Function


def test_call():
    assert repr(Call('foo', 'bar')) == 'foo -> bar'
    assert repr(Call('bar', Function('baz', 'foo'))) == 'bar -> baz.foo()'

    bar = Call('bar', 'baz', children=[
        Call('baz', 'quux', children=[
            Call('quux', Function('fred', 'fire', 'a', 'b'))
        ]),
        Call('baz', 'thud')
    ])

    assert repr(bar) == '''\
bar -> baz:
  baz -> quux:
    quux -> fred.fire(a, b)
  baz -> thud'''
