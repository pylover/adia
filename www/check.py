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
    from tests import test_asciicanvas
    from tests import test_mutablestring
    from tests import test_sequence
    from tests import test_diagram

    for module in [
        test_token,
        test_tokenizer,
        test_asciicanvas,
        test_mutablestring,
        test_sequence,
        test_diagram,
    ]:
        for test in runtests(module):
            yield test
