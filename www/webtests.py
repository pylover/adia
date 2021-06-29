def findtests(module):
    global counter
    for k, v in module.__dict__.items():
        if k.startswith('test_'):
            try:
                v()
            except Exception as ex:
                print(k, f'Failed: {ex}')
                raise
            else:
                counter += 1
                print(k, 'Ok')


def run():
    global counter
    counter = 0

    print('Running Dial web tests')
    from tests import test_token
    from tests import test_tokenizer
    from tests import test_mutablestring
    from tests import test_sequence_interpreter

    findtests(test_token)
    findtests(test_tokenizer)
    findtests(test_mutablestring)
    findtests(test_sequence_interpreter)

    print(f'{counter} tests are passed successfully.')
