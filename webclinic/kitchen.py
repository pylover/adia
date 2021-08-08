import io


s = io.StringIO('foo\n  bar\n  baz\n')
index = 0
while True:
    line = s.readline()
    print(index, f'len: {len(line)}', repr(line))
    index += 1
    if not line:
        break

# Brython
"""
0   len: 4   'foo\n'
1   len: 6   '  bar\n'
2   len: 0   ''
"""
# CPython
"""
0 len: 4 'foo\n'
1 len: 6 '  bar\n'
2 len: 5 '  baz'
3 len: 0 ''
"""


def run():
    pass
