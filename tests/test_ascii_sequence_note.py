from dial.ascii import ASCIIDiagramRenderer
from dial.diagram import Diagram

from .helpers import eqdia


def test_asciisequence_multilinenote():
    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        @foo: |
            THUD Qux Quux
            Foo Bar Baz
        @foo ~ bar: |
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam
            sollicitudin sem eget ligula imperdiet, sit amet gravida mi tempor.

    '''))
    assert eqdia(str(r.render()), '''
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


def test_asciisequence_note():
    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        @foo: THUD Qux Quux
        @foo ~ bar: Bar
        @foo: FOO
        @foo: THUD
        @bar ~ baz: Bar Baz Quux
        @foo ~ baz: FooBaz
    '''))
    assert eqdia(str(r.render()), '''
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
