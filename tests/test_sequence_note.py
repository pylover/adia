from dial import Diagram

from .helpers import eqdia


def test_sequence_multilinenote():
    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        @foo: |
            THUD Qux Quux
            Foo Bar Baz
        @foo ~ bar: |
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam
            sollicitudin sem eget ligula imperdiet, sit amet gravida mi tempor.

    ''')
    assert eqdia(d.renders(), '''
    ...........................................................................
    . DIAGRAM: Foo                                                            .
    . version: 1.0                                                            .
    .                                                                         .
    . +-----+                                                         +-----+ .
    . | foo |                                                         | bar | .
    . +-----+                                                         +-----+ .
    .    |                                                               |    .
    . -----------------                                                  |    .
    . | THUD Qux Quux |                                                  |    .
    . | Foo Bar Baz   |                                                  |    .
    . -----------------                                                  |    .
    . ----------------------------------------------------------------------- .
    . | Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam     | .
    . | sollicitudin sem eget ligula imperdiet, sit amet gravida mi tempor. | .
    . ----------------------------------------------------------------------- .
    .    |                                                               |    .
    . +-----+                                                         +-----+ .
    . | foo |                                                         | bar | .
    . +-----+                                                         +-----+ .
    .                                                                         .
    ...........................................................................
    ''')


def test_sequence_note():
    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        @foo: THUD Qux Quux
        @foo ~ bar: Bar
        @foo: FOO
        @foo: THUD
        @bar ~ baz: Bar Baz Quux
        @foo ~ baz: FooBaz
    ''')
    assert eqdia(d.renders(), '''
    .......................................
    . DIAGRAM: Foo                        .
    . version: 1.0                        .
    .                                     .
    . +-----+            +-----+  +-----+ .
    . | foo |            | bar |  | baz | .
    . +-----+            +-----+  +-----+ .
    .    |                  |        |    .
    . -----------------     |        |    .
    . | THUD Qux Quux |     |        |    .
    . -----------------     |        |    .
    . --------------------------     |    .
    . | Bar                    |     |    .
    . --------------------------     |    .
    . -------               |        |    .
    . | FOO |               |        |    .
    . -------               |        |    .
    . --------              |        |    .
    . | THUD |              |        |    .
    . --------              |        |    .
    .    |               ---------------- .
    .    |               | Bar Baz Quux | .
    .    |               ---------------- .
    . ----------------------------------- .
    . | FooBaz                          | .
    . ----------------------------------- .
    .    |                  |        |    .
    . +-----+            +-----+  +-----+ .
    . | foo |            | bar |  | baz | .
    . +-----+            +-----+  +-----+ .
    .                                     .
    .......................................
    ''')
