from .token import TOKEN_NAMES, EXACT_TOKENS_DICT


class InterpreterError(Exception):
    def __init__(self, interpreter, token, msg):
        filename = interpreter.tokenizer.filename or 'String'

        super().__init__(
            f'File "{filename}", '
            f'Interpreter {interpreter.__class__.__name__}, '
            f'line {token.start[0]}, col {token.start[1]}\n'
            f'{msg}'
        )


class BadAttribute(InterpreterError):
    def __init__(self, interpreter, token, attr):
        super().__init__(interpreter, token, f'Invalid attribute: {attr}.')


class BadSyntax(InterpreterError):
    def __init__(self, interpreter, token):
        got = TOKEN_NAMES[token.type]
        if token.string.strip():
            gotstr = f' "{token.string}"'
        else:
            gotstr = ''

        validtokens = [
            EXACT_TOKENS_DICT.get(i, TOKEN_NAMES[i])
            for i in interpreter.state.keys()
        ]
        expected = 'Expected Nothing'
        if len(validtokens) > 1:
            expected = f'Expected one of `{"|".join(validtokens)}`'
        elif len(validtokens) == 1:
            expected = f'Expected `{validtokens[0]}`'

        super().__init__(
            interpreter, token, f'{expected}, got: {got}{gotstr}.'
        )
