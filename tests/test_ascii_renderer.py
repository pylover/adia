from dial.sequence import Module
from dial.ascii.renderer import ModulePlan, ItemStartPlan, ItemEndPlan, LEFT, \
    RIGHT


def test_asciirenderer_moduleplan():
    p = ModulePlan(Module('foo'))
    assert repr(p) == 'ModulePlan: foo'


def test_asciirenderer_itemplans():
    class Item:
        def __repr__(self):
            return 'foo -> bar'

    item = Item()
    p = ItemStartPlan(item, Module('foo'), Module('bar'), RIGHT, 0)
    assert repr(p) == '~~~> foo -> bar'

    p = ItemEndPlan(item, Module('foo'), Module('bar'), RIGHT, 0)
    assert repr(p) == '<--- foo -> bar'
