from adia import Diagram

from .helpers import eqdia


def test_sequence_selfcall():
    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        foo -> foo: init()
          foo -> foo: hey
        bar -> bar:
    ''')
    assert eqdia(d, '''
    ...............................
    . DIAGRAM: Foo                .
    . version: 1.0                .
    .                             .
    . +-----+         +-----+     .
    . | foo |         | bar |     .
    . +-----+         +-----+     .
    .    |               |        .
    .    |~~~init()~~~+  |        .
    .    |~~~hey~~~+  |  |        .
    .    |         |  |  |        .
    .    |<--------+  |  |        .
    .    |<-----------+  |        .
    .    |               |        .
    .    |               |~~~~~~+ .
    .    |               |      | .
    .    |               |<-----+ .
    .    |               |        .
    . +-----+         +-----+     .
    . | foo |         | bar |     .
    . +-----+         +-----+     .
    ...............................
    ''')


def test_sequence_selfcall_returntext():
    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence:

        foo -> foo: init() => error/zero
        bar -> bar: => Exception
    ''')
    assert eqdia(d, '''
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
    ............................................
    ''')


def test_sequence_selfcall_issue6():
    d = Diagram('''
        diagram: foo
        sequence:

        foo -> bar: ensure()
          if: not bar.is_connected
            bar -> bar: connect()
    ''')
    assert eqdia(d, '''
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
    ...............................................
    ''')


def test_sequence_condition_inside_selfcall_issue5_test1():
    d = Diagram('''
        diagram: foo
        sequence:

        bar -> bar: connect()
          if: not bar.is_connected
    ''')
    assert eqdia(d, '''
    ...............................
    . DIAGRAM: foo                .
    .                             .
    . +-----+                     .
    . | bar |                     .
    . +-----+                     .
    .    |                        .
    .    |~~~connect()~~~+        .
    .    |               |        .
    . *************************** .
    . * if not bar.is_connected * .
    . *************************** .
    . *************************** .
    . * end if                  * .
    . *************************** .
    .    |               |        .
    .    |<--------------+        .
    .    |                        .
    . +-----+                     .
    . | bar |                     .
    . +-----+                     .
    ...............................
    ''')


def test_sequence_condition_inside_selfcall_issue5_test2():
    d = Diagram('''
        diagram: foo
        sequence:

        bar -> bar: connect()
          if: not bar.is_connected
            bar -> baz: Lorem ipsum dolor sit amet
    ''')
    assert eqdia(d, '''
    .............................................
    . DIAGRAM: foo                              .
    .                                           .
    . +-----+                           +-----+ .
    . | bar |                           | baz | .
    . +-----+                           +-----+ .
    .    |                                 |    .
    .    |~~~connect()~~~+                 |    .
    .    |               |                 |    .
    . ***************************************** .
    . * if not bar.is_connected               * .
    . ***************************************** .
    .    |               |                 |    .
    .    |~~~Lorem ipsum dolor sit amet~~~>|    .
    .    |               |                 |    .
    .    |<--------------------------------|    .
    .    |               |                 |    .
    . ***************************************** .
    . * end if                                * .
    . ***************************************** .
    .    |               |                 |    .
    .    |<--------------+                 |    .
    .    |                                 |    .
    . +-----+                           +-----+ .
    . | bar |                           | baz | .
    . +-----+                           +-----+ .
    .............................................
    ''')


def test_sequence_condition_inside_selfcall_issue5_test3():
    d = Diagram('''
        diagram: foo
        sequence:

        foo -> bar: ensure()
          bar -> bar: connect()
            if: not bar.is_connected
    ''')
    assert eqdia(d, '''
    ...............................................
    . DIAGRAM: foo                                .
    .                                             .
    . +-----+         +-----+                     .
    . | foo |         | bar |                     .
    . +-----+         +-----+                     .
    .    |               |                        .
    .    |~~~ensure()~~~>|                        .
    .    |               |~~~connect()~~~+        .
    .    |               |               |        .
    .    |            *************************** .
    .    |            * if not bar.is_connected * .
    .    |            *************************** .
    .    |            *************************** .
    .    |            * end if                  * .
    .    |            *************************** .
    .    |               |               |        .
    .    |               |<--------------+        .
    .    |<--------------|                        .
    .    |               |                        .
    . +-----+         +-----+                     .
    . | foo |         | bar |                     .
    . +-----+         +-----+                     .
    ...............................................
    ''')


def test_sequence_condition_inside_selfcall_issue5_test4():
    d = Diagram('''
        diagram: foo
        sequence:

        foo -> bar: ensure()
          bar -> bar: connect()
            if: not bar.is_connected
                bar -> baz
    ''')
    assert eqdia(d, '''
    ...............................................
    . DIAGRAM: foo                                .
    .                                             .
    . +-----+         +-----+             +-----+ .
    . | foo |         | bar |             | baz | .
    . +-----+         +-----+             +-----+ .
    .    |               |                   |    .
    .    |~~~ensure()~~~>|                   |    .
    .    |               |~~~connect()~~~+   |    .
    .    |               |               |   |    .
    .    |            *************************** .
    .    |            * if not bar.is_connected * .
    .    |            *************************** .
    .    |               |               |   |    .
    .    |               |~~~~~~~~~~~~~~~~~~>|    .
    .    |               |               |   |    .
    .    |               |<------------------|    .
    .    |               |               |   |    .
    .    |            *************************** .
    .    |            * end if                  * .
    .    |            *************************** .
    .    |               |               |   |    .
    .    |               |<--------------+   |    .
    .    |<--------------|                   |    .
    .    |               |                   |    .
    . +-----+         +-----+             +-----+ .
    . | foo |         | bar |             | baz | .
    . +-----+         +-----+             +-----+ .
    ...............................................
    ''')


def test_sequence_loop_over_selfcall_issue44():
    d = Diagram('''
        diagram: foo
        sequence:
        while: Lorem ipsum
          foo -> foo

        for: Lorem Ipsum
          foo -> foo
    ''')
    assert eqdia(d, '''
    .........................
    . DIAGRAM: foo          .
    .                       .
    . +-----+               .
    . | foo |               .
    . +-----+               .
    .    |                  .
    . ********************* .
    . * while Lorem ipsum * .
    . ********************* .
    .    |                  .
    .    |~~~~~~+           .
    .    |      |           .
    .    |<-----+           .
    .    |                  .
    . ********************* .
    . * end while         * .
    . ********************* .
    .    |                  .
    . *******************   .
    . * for Lorem Ipsum *   .
    . *******************   .
    .    |                  .
    .    |~~~~~~+           .
    .    |      |           .
    .    |<-----+           .
    .    |                  .
    . *******************   .
    . * end for         *   .
    . *******************   .
    .    |                  .
    . +-----+               .
    . | foo |               .
    . +-----+               .
    .........................
    ''')
