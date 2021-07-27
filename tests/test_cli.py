from bddcli import when, stdout, status, stderr

import dial
from .helpers import eqdia, eqbigstr


OK = 0
ERR = 1


def test_version(app):
    with app():
        assert status == OK
        assert stderr == ''

        when('-V')
        assert status == OK
        assert stdout[:-1] == dial.__version__

        when('--version')
        assert status == OK
        assert stdout[:-1] == dial.__version__


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

    with app(stdin=source):
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
        .                             .
        ..
        ...............................
        ''', offset=8)


def test_inputfile(app, tempstruct):
    source = '''
        diagram: Foo
        sequence:
        foo -> bar: Hello World!
    '''
    temproot = tempstruct(**{
        'foo.dial': source,
    })

    with app(f'{temproot}/foo.dial'):
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
        .                             .
        ..
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
        'foo.dial': source1,
        'baz.dial': source2,
    })

    with app(f'{temproot}/foo.dial {temproot}/baz.dial'):
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
        .                             .
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
        .                             .
        ..
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
        'foo.dial': source1,
        'bad.dial': source2,
        'baz.dial': source3,
    })

    with app(f'{temproot}/foo.dial {temproot}/bad.dial {temproot}/baz.dial'):
        assert eqbigstr(stderr, f'''
            BadSyntax: File "{temproot}/bad.dial", Interpreter: Diagram, line 1, col 0
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
        .                             .
        ..
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
        'foo.dial': source,
    })

    with app(f'-C {temproot} foo.dial'):
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
        .                             .
        ..
        ...............................
        ''', offset=8)


def test_help(app):
    with app('--help'):
        assert stderr == ''
        assert eqbigstr(stdout, '''
            usage: dial [-h] [-V] [-C CHANGE_DIRECTORY] [file [file ...]]

            ASCII diagram language interpreter

            positional arguments:
              file                  File containing dial source code. if not given, the
                                    standard input will be used.

            optional arguments:
              -h, --help            show this help message and exit
              -V, --version
              -C CHANGE_DIRECTORY, --change-directory CHANGE_DIRECTORY
                                    Change the current working directory before executing,
                                    default: ".".
        ''', offset=12)  # noqa
