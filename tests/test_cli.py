from bddcli import when, stdout, status, stderr

import adia
from .helpers import eqdia, eqbigstr


OK = 0
ERR = 1


def test_version(app):
    with app():
        assert status == OK
        assert stderr == ''

        when('-V')
        assert status == OK
        assert stdout[:-1] == adia.__version__

        when('--version')
        assert status == OK
        assert stdout[:-1] == adia.__version__


def test_error(app):
    source = 'invalid'

    with app(stdin=source):
        assert stdout == ''
        assert eqbigstr(stderr, '''
            BadSyntax: File "<stdin>", Interpreter: Diagram, line 1, col 0
            Expected one of `diagram author version sequence`, got: `invalid`.
        ''', offset=12)


def test_standardinput(app):
    source = '''
        diagram: Foo
        sequence:
        foo -> bar: Hello World!
    '''

    with app('--no-rstrip', stdin=source):
        assert eqdia(stdout, '''
        ...............................
        . DIAGRAM: Foo                .
        .                             .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        .    |                   |    .
        .    |~~~Hello World!~~~>|    .
        .    |                   |    .
        .    |<------------------|    .
        .    |                   |    .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        ...............................
        ''', offset=8)


def test_inputfile(app, tempstruct):
    source = '''
        diagram: Foo
        sequence:
        foo -> bar: Hello World!
    '''
    temproot = tempstruct(**{
        'foo.adia': source,
    })

    with app(f'{temproot}/foo.adia'):
        assert stderr == ''
        assert eqdia(stdout, '''
        ...............................
        . DIAGRAM: Foo                .
        .                             .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        .    |                   |    .
        .    |~~~Hello World!~~~>|    .
        .    |                   |    .
        .    |<------------------|    .
        .    |                   |    .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        ...............................
        ''', offset=8)


def test_multiple_inputfiles(app, tempstruct):
    source1 = '''
        diagram: Foo
        sequence:
        foo -> bar: Hello World!
    '''
    source2 = '''
        diagram: Baz
        sequence:
        baz -> bar: Hello World!
    '''

    temproot = tempstruct(**{
        'foo.adia': source1,
        'baz.adia': source2,
    })

    with app(f'{temproot}/foo.adia {temproot}/baz.adia'):
        assert stderr == ''
        assert eqdia(stdout, '''
        ...............................
        . DIAGRAM: Foo                .
        .                             .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        .    |                   |    .
        .    |~~~Hello World!~~~>|    .
        .    |                   |    .
        .    |<------------------|    .
        .    |                   |    .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        ..
        . DIAGRAM: Baz                .
        .                             .
        . +-----+             +-----+ .
        . | baz |             | bar | .
        . +-----+             +-----+ .
        .    |                   |    .
        .    |~~~Hello World!~~~>|    .
        .    |                   |    .
        .    |<------------------|    .
        .    |                   |    .
        . +-----+             +-----+ .
        . | baz |             | bar | .
        . +-----+             +-----+ .
        ...............................
        ''', offset=8)


def test_multiple_inputfiles_error(app, tempstruct):
    source1 = '''
        diagram: Foo
        sequence:
        foo -> bar: Hello World!
    '''
    source2 = 'bad contents'
    source3 = '''
        diagram: Baz
        sequence:
        baz -> bar: Hello World!
    '''

    temproot = tempstruct(**{
        'foo.adia': source1,
        'bad.adia': source2,
        'baz.adia': source3,
    })

    with app(f'{temproot}/foo.adia {temproot}/bad.adia {temproot}/baz.adia'):
        assert eqbigstr(stderr, f'''
            BadSyntax: File "{temproot}/bad.adia", Interpreter: Diagram, line 1, col 0
            Expected one of `diagram author version sequence`, got: `bad`.
        ''', offset=12)  # noqa

        assert eqdia(stdout, '''
        ...............................
        . DIAGRAM: Foo                .
        .                             .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        .    |                   |    .
        .    |~~~Hello World!~~~>|    .
        .    |                   |    .
        .    |<------------------|    .
        .    |                   |    .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        ..
        ...............................
        ''', offset=8)


def test_changedirectory(app, tempstruct):
    source = '''
        diagram: Foo
        sequence:
        foo -> bar: Hello World!
    '''
    temproot = tempstruct(**{
        'foo.adia': source,
    })

    with app(f'-C {temproot} foo.adia'):
        assert stderr == ''
        assert eqdia(stdout, '''
        ...............................
        . DIAGRAM: Foo                .
        .                             .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        .    |                   |    .
        .    |~~~Hello World!~~~>|    .
        .    |                   |    .
        .    |<------------------|    .
        .    |                   |    .
        . +-----+             +-----+ .
        . | foo |             | bar | .
        . +-----+             +-----+ .
        ...............................
        ''', offset=8)
