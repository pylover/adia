from adia.token import Token, AT


def test_token():
    t = Token(AT, '@', (1, 0), (1, 1), '@foo')
    assert repr(t) == 'Token(AT, @, (1, 0), (1, 1), @foo)'
