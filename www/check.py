def runtests(module):
    for k, v in module.__dict__.items():
        if k.startswith('test_'):
            try:
                v()
            except Exception as ex:
                yield f'Failed {k}: {ex}'
                raise ex
            else:
                yield f'OK {k}'


def run():
    from tests import test_token
    from tests import test_tokenizer
    from tests import test_mutablestring
    from tests import test_sequence
    from tests import test_asciicanvas
    from tests import test_asciirenderer
    from tests import test_asciidiagram
    from tests import test_diagram
    from tests import test_ascii_sequence_header
    from tests import test_ascii_sequence_callstack
    from tests import test_ascii_sequence_condition
    from tests import test_ascii_sequence_loop

    for module in [
        test_token,
        test_tokenizer,
        test_mutablestring,
        test_sequence,
        test_diagram,
        test_asciicanvas,
        test_asciirenderer,
        test_asciidiagram,
        test_ascii_sequence_header,
        test_ascii_sequence_callstack,
        test_ascii_sequence_condition,
        test_ascii_sequence_loop,
    ]:
        for test in runtests(module):
            yield test
