from dial import Diagram

from .helpers import eqdia


def test_sequence_selfcall():
    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        foo -> foo: init()
        bar -> bar:
    ''')
    assert eqdia(d.renders(), '''
    ...............................
    . DIAGRAM: Foo                .
    . version: 1.0                .
    .                             .
    . +-----+         +-----+     .
    . | foo |         | bar |     .
    . +-----+         +-----+     .
    .    |               |        .
    .    |~~~init()~~~+  |        .
    .    |            |  |        .
    .    |<-----------+  |        .
    .    |               |        .
    .    |               |~~~~~~+ .
    .    |               |      | .
    .    |               |<-----+ .
    .    |               |        .
    . +-----+         +-----+     .
    . | foo |         | bar |     .
    . +-----+         +-----+     .
    .                             .
    ...............................
    ''')


def test_sequence_selfcall_returntext():
    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        foo -> foo: init() -> error/zero
        bar -> bar: -> Exception
    ''')
    assert eqdia(d.renders(), '''
    ............................................
    . DIAGRAM: Foo                             .
    . version: 1.0                             .
    .                                          .
    . +-----+             +-----+              .
    . | foo |             | bar |              .
    . +-----+             +-----+              .
    .    |                   |                 .
    .    |~~~init()~~~~~~~+  |                 .
    .    |                |  |                 .
    .    |<--error/zero---+  |                 .
    .    |                   |                 .
    .    |                   |~~~~~~~~~~~~~~~+ .
    .    |                   |               | .
    .    |                   |<--Exception---+ .
    .    |                   |                 .
    . +-----+             +-----+              .
    . | foo |             | bar |              .
    . +-----+             +-----+              .
    .                                          .
    ............................................
    ''')


def test_sequence_selfcall_issue_6():
    d = Diagram('''
        diagram: foo
        sequence:

        foo -> bar: ensure()
          if: not bar.is_connected
            bar -> bar: connect()
    ''')
    assert eqdia(d.renders(), '''
    ...............................................
    . DIAGRAM: foo                                .
    .                                             .
    . +-----+         +-----+                     .
    . | foo |         | bar |                     .
    . +-----+         +-----+                     .
    .    |               |                        .
    .    |~~~ensure()~~~>|                        .
    .    |               |                        .
    .    |            *************************** .
    .    |            * if not bar.is_connected * .
    .    |            *************************** .
    .    |               |                        .
    .    |               |~~~connect()~~~+        .
    .    |               |               |        .
    .    |               |<--------------+        .
    .    |               |                        .
    .    |            *************************** .
    .    |            * end if                  * .
    .    |            *************************** .
    .    |               |                        .
    .    |<--------------|                        .
    .    |               |                        .
    . +-----+         +-----+                     .
    . | foo |         | bar |                     .
    . +-----+         +-----+                     .
    .                                             .
    ...............................................
    ''')
