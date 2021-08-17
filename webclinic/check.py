from browser import bind, self


OK = True
FAILURE = False
ok_counter = 0
fail_counter = 0


def run_module_tests(module):
    for k, v in module.__dict__.items():
        if not k.startswith('test_'):
            continue

        try:
            v()
        except Exception as ex:
            yield k, FAILURE, ex
        else:
            yield k, OK, v


def run():
    from tests import test_api
    from tests import test_canvas
    from tests import test_diagram
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
    from tests import test_sequence_selfcall
    from tests import test_token
    from tests import test_tokenizer

    for module in [
        test_api,
        test_canvas,
        test_diagram,
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
        test_sequence_selfcall,
        test_token,
        test_tokenizer,
    ]:
        for test in run_module_tests(module):
            yield test


def report(msg, status=OK):
    self.send({
        'message': msg,
        'status': status
    })


@bind(self, 'message')
def message(ev):
    global ok_counter, fail_counter

    if ev.data != 'start':
        report(f'Invalid message: {ev.data}', FAILURE)

    report('Check process started successfully')

    for test, status, details in run():
        if status:
            ok_counter += 1
        else:
            fail_counter += 1

        report(test, status)

    report(f'{ok_counter} passed, {fail_counter} failed.', fail_counter == 0)
