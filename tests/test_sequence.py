from abcdia import parse, Call


def test_simple_call():
    doc = parse('foo: bar')
    assert len(doc) == 1
    assert isinstance(doc[0], SequenceDiagram)
    assert doc[0] == [
        Call('foo', 'bar'),
    ]
