from .token import Token


class Call(Token):
    def __init__(self, caller, callee, function):
        self.caller = caller
        self.callee = callee
        self.function = function
