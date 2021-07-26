from dial import Diagram

from .helpers import eqdia


def test_readme_quickstart():
    d = Diagram('''
        diagram: Foo

        sequence:

        foo -> bar: Hello World!

    ''')
    assert eqdia(d.renders(), '''
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
    ...............................
    ''')


def test_readme_complte_examaple():
    d = Diagram('''
        diagram: Authentication
        version: 1.0
        author: pylover

        sequence: Login/Logout
        alice.title: Alice
        bob.title: Bob
        db.title: Database

        # Login
        @alice ~ bob: Alice tries to authenticate herself
        alice -> bob: authenticate(email, password) -> token
          if: db is null
            bob -> db: initialize() -> db
          elif: db.is_connected()
            bob -> db: keepalive()
          else:
            while: not db.is_connected()
              bob -> db: connect()

          bob -> bob: create_token() -> token

        @alice: |
          Alice decides to
          store the newly
          received Token
          in a safe place.
        alice -> alice: store(token)

        # Logout
        @alice ~ bob: Alice tries to logout
        alice -> bob: logout(token)
          bob -> db: delete(token)
          for: each token in db
            bob -> db: delete(token)
    ''')

    assert eqdia(d.renders(), '''
    ...............................................................................
    . DIAGRAM: Authentication                                                     .
    . author: pylover                                                             .
    . version: 1.0                                                                .
    .                                                                             .
    .                                                                             .
    . SEQUENCE: Login/Logout                                                      .
    .                                                                             .
    . +-------+                             +-----+                 +-----------+ .
    . | Alice |                             | Bob |                 | Database  | .
    . +-------+                             +-----+                 +-----------+ .
    .     |                                    |                          |       .
    . ---------------------------------------------                       |       .
    . | Alice tries to authenticate herself       |                       |       .
    . ---------------------------------------------                       |       .
    .     |                                    |                          |       .
    .     |~~~authenticate(email, password)~~~>|                          |       .
    .     |                                    |                          |       .
    .     |                                 ************************************* .
    .     |                                 * if db is null                     * .
    .     |                                 ************************************* .
    .     |                                    |                          |       .
    .     |                                    |~~~initialize()~~~~~~~~~~>|       .
    .     |                                    |                          |       .
    .     |                                    |<--db---------------------|       .
    .     |                                    |                          |       .
    .     |                                 ************************************* .
    .     |                                 * elif db.is_connected()            * .
    .     |                                 ************************************* .
    .     |                                    |                          |       .
    .     |                                    |~~~keepalive()~~~~~~~~~~~>|       .
    .     |                                    |                          |       .
    .     |                                    |<-------------------------|       .
    .     |                                    |                          |       .
    .     |                                 ************************************* .
    .     |                                 * else                              * .
    .     |                                 ************************************* .
    .     |                                 ************************************* .
    .     |                                 * while not db.is_connected()       * .
    .     |                                 ************************************* .
    .     |                                    |                          |       .
    .     |                                    |~~~connect()~~~~~~~~~~~~~>|       .
    .     |                                    |                          |       .
    .     |                                    |<-------------------------|       .
    .     |                                    |                          |       .
    .     |                                 ************************************* .
    .     |                                 * end while                         * .
    .     |                                 ************************************* .
    .     |                                 ************************************* .
    .     |                                 * end if                            * .
    .     |                                 ************************************* .
    .     |                                    |                          |       .
    .     |                                    |~~~create_token()~~~+     |       .
    .     |                                    |                    |     |       .
    .     |                                    |<--token------------+     |       .
    .     |<--token----------------------------|                          |       .
    .     |                                    |                          |       .
    . --------------------                     |                          |       .
    . | Alice decides to |                     |                          |       .
    . | store the newly  |                     |                          |       .
    . | received Token   |                     |                          |       .
    . | in a safe place. |                     |                          |       .
    . --------------------                     |                          |       .
    .     |                                    |                          |       .
    .     |~~~store(token)~~~+                 |                          |       .
    .     |                  |                 |                          |       .
    .     |<-----------------+                 |                          |       .
    .     |                                    |                          |       .
    . ---------------------------------------------                       |       .
    . | Alice tries to logout                     |                       |       .
    . ---------------------------------------------                       |       .
    .     |                                    |                          |       .
    .     |~~~logout(token)~~~~~~~~~~~~~~~~~~~>|                          |       .
    .     |                                    |~~~delete(token)~~~~~~~~~>|       .
    .     |                                    |                          |       .
    .     |                                    |<-------------------------|       .
    .     |                                    |                          |       .
    .     |                                 ************************************* .
    .     |                                 * for each token in db              * .
    .     |                                 ************************************* .
    .     |                                    |                          |       .
    .     |                                    |~~~delete(token)~~~~~~~~~>|       .
    .     |                                    |                          |       .
    .     |                                    |<-------------------------|       .
    .     |                                    |                          |       .
    .     |                                 ************************************* .
    .     |                                 * end for                           * .
    .     |                                 ************************************* .
    .     |                                    |                          |       .
    .     |<-----------------------------------|                          |       .
    .     |                                    |                          |       .
    . +-------+                             +-----+                 +-----------+ .
    . | Alice |                             | Bob |                 | Database  | .
    . +-------+                             +-----+                 +-----------+ .
    .                                                                             .
    ...............................................................................
    ''')  # noqa
