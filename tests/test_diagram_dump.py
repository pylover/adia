from io import StringIO

from dial import Diagram
from dial.exceptions import BadSyntax

from .helpers import raises, eqbigstr


def test_diagram_full():
    s = '''
        diagram: HTTPLoad
        version: 1.0
        author: Vahid Mardani

        sequence: Event Loop

        cli -> httpd: err_t start(httpd*)
          for: i in range(forks)
            httpd -> ev: server_start(evs*)
              ev -> tcp: int listen(port)
              ev -> ev_epoll: err_t server_init(evs*)
              ev -> ev_common: err_t fork(evs*, epoll_loop)
              if: err
                ev -> ev_epoll: server_deinit(evs*)
                @ev: Error
              else: ok
                @ev: Ok
        cli -> httpd: err_t join(httpd*)
    '''

    diagram = Diagram(StringIO(s))
    assert eqbigstr(diagram.dumps(), s)


def test_diagram_parsefile():
    s = '''
        diagram: Foo
        version: 1.0
        author: thud

        sequence: Bar Baz

        # Modules
        bar.title: Bar
        foo.type: Actor

        foo -> bar
          bar -> baz: init()
    '''

    diagram = Diagram(StringIO(s))
    assert eqbigstr(diagram.dumps(), s)


def test_diagram_comment():
    s = '''
        diagram: Foo
        # This is Comment
    '''
    assert eqbigstr(Diagram(s).dumps(), '''
        diagram: Foo
    ''')


def test_diagram_repr():
    diagram = Diagram()
    assert repr(diagram) == 'Diagram: Untitled Diagram'

    diagram.parseline('diagram: Foo')
    assert repr(diagram) == 'Diagram: Foo'


def test_diagram_emptyline():
    s = 'diagram: foo\n  \n'
    diagram = Diagram(StringIO(s))
    assert diagram.dumps() == 'diagram: foo\n'

    s = 'sequence: foo\n  \n'
    diagram = Diagram(StringIO(s))
    assert diagram.dumps() == 'diagram: Untitled Diagram\n\nsequence: foo\n'


def test_diagram_attr_error():
    s = '''
        diagram: Foo
        invalid: invalid
    '''
    with raises(BadSyntax) as e:
        Diagram(s)
    assert eqbigstr(e.value, '''
        File "String", Interpreter Diagram, line 3, col 8
        Expected one of `diagram author version sequence`, got: `invalid`.
    ''')
