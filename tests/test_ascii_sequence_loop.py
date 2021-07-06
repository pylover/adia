from dial.ascii import ASCIIDiagramRenderer
from dial.diagram import Diagram

from .helpers import eqdia


def test_asciisequence_loop():
    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        for: i in 0~10
          b -> a
          if: yes
            while: True
              a -> c
    '''))
    assert eqdia(str(r.render()), '''
    ........................
    . DIAGRAM: Foo         .
    . version: 1.0         .
    .                      .
    . +---+ +---+    +---+ .
    . | b | | a |    | c | .
    . +---+ +---+    +---+ .
    .   |     |        |   .
    . ******************** .
    . * for i in 0~10    * .
    . ******************** .
    .   |     |        |   .
    .   |~~~~>|        |   .
    .   |     |        |   .
    .   |<----|        |   .
    .   |     |        |   .
    .   |   ************** .
    .   |   * if yes     * .
    .   |   ************** .
    .   |   ************** .
    .   |   * while True * .
    .   |   ************** .
    .   |     |        |   .
    .   |     |~~~~~~~>|   .
    .   |     |        |   .
    .   |     |<-------|   .
    .   |     |        |   .
    .   |   ************** .
    .   |   * end while  * .
    .   |   ************** .
    .   |   ************** .
    .   |   * end if     * .
    .   |   ************** .
    . ******************** .
    . * end for          * .
    . ******************** .
    .   |     |        |   .
    . +---+ +---+    +---+ .
    . | b | | a |    | c | .
    . +---+ +---+    +---+ .
    .                      .
    ........................
    ''')


def test_asciisequence_loop_isolation():
    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        foo -> bar:
        for: i in range(10)
         a -> b: hello()

    '''))
    assert eqdia(str(r.render()), '''
    ..........................................
    . DIAGRAM: Foo                           .
    . version: 1.0                           .
    .                                        .
    . +-----+ +-----+ +---+            +---+ .
    . | foo | | bar | | a |            | b | .
    . +-----+ +-----+ +---+            +---+ .
    .    |       |      |                |   .
    .    |~~~~~~>|      |                |   .
    .    |       |      |                |   .
    .    |<------|      |                |   .
    .    |       |      |                |   .
    .    |       |    ********************** .
    .    |       |    * for i in range(10) * .
    .    |       |    ********************** .
    .    |       |      |                |   .
    .    |       |      |~~~hello()~~~~~>|   .
    .    |       |      |                |   .
    .    |       |      |<---------------|   .
    .    |       |      |                |   .
    .    |       |    ********************** .
    .    |       |    * end for            * .
    .    |       |    ********************** .
    .    |       |      |                |   .
    . +-----+ +-----+ +---+            +---+ .
    . | foo | | bar | | a |            | b | .
    . +-----+ +-----+ +---+            +---+ .
    .                                        .
    ..........................................
    ''')
