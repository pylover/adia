from adia.sequence import Module
from adia.renderer import ModulePlan, ItemStartPlan, ItemEndPlan, LEFT, RIGHT


def test_moduleplan():
    p = ModulePlan(Module('foo'))
    assert repr(p) == 'ModulePlan: foo'


def test_itemplans():
    class Item:
        def __repr__(self):
            return 'foo -> bar'

    item = Item()
    p = ItemStartPlan(item, Module('foo'), Module('bar'), RIGHT, 0)
    assert repr(p) == '~~~> foo -> bar'

    p = ItemEndPlan(item, Module('foo'), Module('bar'), LEFT, 0)
    assert repr(p) == '<--- foo -> bar'
