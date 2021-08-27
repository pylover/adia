from adia import Diagram

from .helpers import eqdia


def test_sequence_loop():
    d = Diagram('''
        sequence:

        for: i in 0~10
          b -> a
          if: yes
            while: True
              a -> c
    ''')
    assert eqdia(d, '''
    ........................
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
    ........................
    ''')


def test_sequence_loop_isolation():
    d = Diagram('''
        sequence:

        foo -> bar:
        for: i in range(10)
         a -> b: hello()

    ''')
    assert eqdia(d, '''
    ..........................................
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
    ..........................................
    ''')
