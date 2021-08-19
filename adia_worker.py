from browser import bind, self

import adia


@bind(self, 'message')
def message(ev):
    request = ev.data

    if request.startswith('?version'):
        self.send({'version': adia.__version__})
        return

    result = {}
    try:
        result['diagram'] = adia.diagram(request)
    except adia.BadSyntax as ex:
        result['error'] = f'Syntax Error: {ex}'
    except adia.BadAttribute as ex:
        result['error'] = f'Attribute Error: {ex}'
    except Exception as ex:
        result['error'] = f'Unhandled Error: {ex}'
    finally:
        self.send(result)
