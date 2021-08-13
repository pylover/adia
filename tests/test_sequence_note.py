from adia import Diagram

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
    assert eqdia(d, '''
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
    assert eqdia(d, '''
    .....................................
    . DIAGRAM: Foo                      .
    . version: 1.0                      .
    .                                   .
    . +-----+          +-----+  +-----+ .
    . | foo |          | bar |  | baz | .
    . +-----+          +-----+  +-----+ .
    .    |                |        |    .
    . -----------------   |        |    .
    . | THUD Qux Quux |   |        |    .
    . -----------------   |        |    .
    . ------------------------     |    .
    . | Bar                  |     |    .
    . ------------------------     |    .
    . -------             |        |    .
    . | FOO |             |        |    .
    . -------             |        |    .
    . --------            |        |    .
    . | THUD |            |        |    .
    . --------            |        |    .
    .    |             ---------------- .
    .    |             | Bar Baz Quux | .
    .    |             ---------------- .
    . --------------------------------- .
    . | FooBaz                        | .
    . --------------------------------- .
    .    |                |        |    .
    . +-----+          +-----+  +-----+ .
    . | foo |          | bar |  | baz | .
    . +-----+          +-----+  +-----+ .
    .....................................
    ''')


def test_sequence_note_issue_8():
    d = Diagram('''
        diagram: Authentication
        version: 1.0
        author: pylover

        sequence: Login
        alice.title: Alice
        bob.title: Bob
        db.title: Database

        @alice ~ bob: Alice tries to login
        alice -> bob: login() => token
          @db: TCP Connection
          bob -> db: connect()

        @alice: Alice tries to login
    ''')
    assert eqdia(d, '''
    ............................................................
    . DIAGRAM: Authentication                                  .
    . author: pylover                                          .
    . version: 1.0                                             .
    .                                                          .
    .                                                          .
    . SEQUENCE: Login                                          .
    .                                                          .
    . +-------+               +-----+       +-----------+      .
    . | Alice |               | Bob |       | Database  |      .
    . +-------+               +-----+       +-----------+      .
    .     |                      |                |            .
    . -------------------------------             |            .
    . | Alice tries to login        |             |            .
    . -------------------------------             |            .
    .     |                      |                |            .
    .     |~~~login()~~~~~~~~~~~>|                |            .
    .     |                      |                |            .
    .     |                      |          ------------------ .
    .     |                      |          | TCP Connection | .
    .     |                      |          ------------------ .
    .     |                      |                |            .
    .     |                      |~~~connect()~~~>|            .
    .     |                      |                |            .
    .     |                      |<---------------|            .
    .     |<--token--------------|                |            .
    .     |                      |                |            .
    . ------------------------   |                |            .
    . | Alice tries to login |   |                |            .
    . ------------------------   |                |            .
    .     |                      |                |            .
    . +-------+               +-----+       +-----------+      .
    . | Alice |               | Bob |       | Database  |      .
    . +-------+               +-----+       +-----------+      .
    ............................................................
    ''')
