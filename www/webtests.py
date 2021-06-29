def findtests(module):
    for k, v in module.__dict__.items():
        if k.startswith('test_'):
            print(k, '...', end='')
            v()
            print('Ok')


def run():
    print('Running Dial web tests')
    from tests import test_mutablestring
    from tests import test_sequence_interpreter
    from tests import test_token
    from tests import test_tokenizer

    findtests(test_mutablestring)
    findtests(test_sequence_interpreter)
    findtests(test_token)
    findtests(test_tokenizer)
