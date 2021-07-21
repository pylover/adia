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
    from tests import test_api
    from tests import test_canvas
    from tests import test_diagram_dump
    from tests import test_diagram_header
    from tests import test_lazyattr
    from tests import test_mutablestring
    from tests import test_readme
    from tests import test_renderer
    from tests import test_sequence_callstack
    from tests import test_sequence_condition
    from tests import test_sequence_header
    from tests import test_sequence_interpreter
    from tests import test_sequence_loop
    from tests import test_sequence_note
    from tests import test_token
    from tests import test_tokenizer

    for module in [
        test_api,
        test_canvas,
        test_diagram_dump,
        test_diagram_header,
        test_lazyattr,
        test_mutablestring,
        test_readme,
        test_renderer,
        test_sequence_callstack,
        test_sequence_condition,
        test_sequence_header,
        test_sequence_interpreter,
        test_sequence_loop,
        test_sequence_note,
        test_token,
        test_tokenizer,
    ]:
        for test in runtests(module):
            yield test
