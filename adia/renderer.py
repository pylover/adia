import io
import itertools

from .sequence import SequenceDiagram, Call, Condition, Loop, Note
from .canvas import Canvas
from .constants import LEFT, RIGHT
from .renderingplans import ModulePlan, ItemStartPlan, ItemEndPlan, \
    ConditionStartPlan, ConditionEndPlan, NotePlan


def twiniter(items):
    if not hasattr(items, '__next__'):
        items = iter(items)

    f = None
    try:
        f = next(items)
        while True:
            n = next(items)
            yield f, n
            f = n
    except StopIteration:
        yield f, None


class Renderer:
    def __init__(self, diagram, canvas=None):
        self._repeats = set()
        self.diagram = diagram

        if canvas is None:
            self.canvas = Canvas()
        else:
            self.canvas = canvas

    def register_repeat(self, col, char):
        self._repeats.add((col, char))

    def unregister_repeat(self, col, char):
        self._repeats.remove((col, char))

    def _render_emptyline(self):
        for col, char in self._repeats:
            self.canvas.set_char(col, self.row, char)

    def _extend(self, i):
        self.canvas.extendbottom(i)

    @property
    def row(self):
        return self.canvas.rows - 1

    def _render_header(self):
        dia = self.diagram
        self._extend(1)
        self.canvas.write_textline(0, self.row, f'DIAGRAM: {dia.title}')

        if dia.author:
            self._extend(1)
            self.canvas.write_textline(0, self.row, f'author: {dia.author}')

        if dia.version:
            self._extend(1)
            self.canvas.write_textline(0, self.row, f'version: {dia.version}')

    def render(self):
        self._render_header()

        for unit in self.diagram:
            if isinstance(unit, SequenceDiagram):
                SequenceRenderer(unit, self.canvas).render()

    def _dumplines(self, rstrip):
        for line in self.canvas:
            line = str(line)
            if rstrip:
                line = line.rstrip()

            yield f'{line}\n'

    def dump(self, filelike, rstrip=True):
        self.render()

        for line in self._dumplines(rstrip):
            filelike.write(line)

    def dumps(self, rstrip=True):
        out = io.StringIO()
        self.dump(out, rstrip)

        # Trailing new line is not interested in dump string
        return out.getvalue()[:-1]


class SequenceRenderer(Renderer):
    _moduleplans = None
    _moduleplans_dict = None
    _itemplans = None

    def _planmodules(self):
        self._moduleplans = []
        self._moduleplans_dict = {}
        for m in self.diagram.modules_order:
            module = ModulePlan(self.diagram.modules[m], lpad=1, rpad=1)
            self._moduleplans.append(module)
            self._moduleplans_dict[m] = module

        for k, v in self.diagram.modules.items():
            if k not in self._moduleplans_dict:
                module = ModulePlan(self.diagram.modules[k], lpad=1, rpad=1)
                self._moduleplans.append(module)
                self._moduleplans_dict[k] = module

        if self._moduleplans:
            self._moduleplans[0].lpad = 0
            self._moduleplans[-1].rpad = 0

    def _fromto_modules(self, from_, to, reverse=False):
        capt = False

        it = self._moduleplans
        if reverse:
            it = reversed(it)

        for m, nm in twiniter(it):
            if not capt and m is not from_:
                continue

            if m is from_:
                capt = True

            if capt:
                if m is to:
                    yield m, None
                    return
                yield m, nm

    def _availspacefor_call(self, from_, to, reverse=False):
        result = 0
        for m, nm in self._fromto_modules(from_, to, reverse):
            result += m.boxlen
            if nm is None:
                continue

            if reverse:
                result += max(m.lpad, nm.rpad)
            else:
                result += max(m.rpad, nm.lpad)

        if from_:
            result -= from_.boxlen // 2 + 1

        if to:
            result -= to.boxlen // 2 + 1

        result -= 7
        return 0 if result < 0 else result

    def _availspacefor_condition(self, from_, to):
        result = 0
        for m, nm in self._fromto_modules(from_, to, False):
            if m is None:
                break

            result += m.boxlen
            if nm is None:
                continue

            result += max(m.rpad, nm.lpad)

        result -= 4
        if result < 0:
            return 0

        return result

    def _availspacefor_note(self, from_, to):
        result = 0
        single = False

        if to is None:
            single = True
            try:
                to = self._moduleplans[self._moduleplans.index(from_) + 1]
            except IndexError:
                to = None

        if to is None:
            result += from_.boxlen
        else:
            for m, nm in self._fromto_modules(from_, to, False):
                result += m.boxlen
                if nm is None:
                    continue

                result += max(m.rpad, nm.lpad)

        if single and to is not None:
            result -= to.boxlen

        result -= 4

        return result

    def _find_condition_startend(self, children):
        items = [(
            self._moduleplans.index(i.caller),
            self._moduleplans.index(i.callee))
            for i in children if isinstance(i, ItemStartPlan)]

        items = sorted(list(set(itertools.chain(*items))))
        start, end = items[0], items[-1]
        return self._moduleplans[start], self._moduleplans[end], start, end

    def _plancondition(self, item, level):
        last, start, end = None, None, None
        if self._itemplans:
            last = self._itemplans[-1]
            if isinstance(last, ConditionEndPlan) and \
                    item.kind not in ('if', 'for', 'while'):
                old = self._itemplans.pop()
                start = old.startmodule
                end = old.endmodule

        condstart_plan = ConditionStartPlan(item, start, end, level)
        self._itemplans.append(condstart_plan)

        if len(item):
            self._recurse(item, level + 1)

        s = self._itemplans.index(condstart_plan) + 1
        if len(self._itemplans) > s:
            start, end, si, ei = \
                self._find_condition_startend(self._itemplans[s:])

            for p in self._itemplans[s::-1]:
                if p.level > level:
                    continue

                if p.startmodule is None:
                    p.startmodule = start
                else:
                    mi = self._moduleplans.index(p.startmodule)
                    if mi > si:
                        p.startmodule = start
                    elif mi < si:
                        start = p.startmodule

                if p.endmodule is None:
                    p.endmodule = end
                else:
                    mi = self._moduleplans.index(p.endmodule)
                    if mi < ei:
                        p.endmodule = end
                    elif mi > si:
                        end = p.endmodule

                if p.kind in ('if', 'for', 'while'):
                    break

        elif isinstance(last, (ItemStartPlan, ItemEndPlan)):
            if start is None:
                start = last.caller
                condstart_plan.startmodule = start

            if end is None:
                end = last.callee
                condstart_plan.endmodule = end

        if start is not None and condstart_plan.singlemodule:
            start.rpad = max(
                start.rpad,
                (condstart_plan.textwidth - start.boxlen) + 4
            )
        else:
            avail = self._availspacefor_condition(start, end)
            if condstart_plan.textwidth > avail:
                amount = condstart_plan.textwidth - avail
                if start:
                    start.rpad += amount

                if end:
                    end.lpad += amount

        condend_plan = ConditionEndPlan(item, start, end, level)
        self._itemplans.append(condend_plan)

        condstart_plan.children = self._itemplans

    def _plannote(self, item, level):
        modules = item.modules
        start = self._moduleplans_dict[modules[0]]
        if len(modules) > 1:
            end = self._moduleplans_dict[modules[1]]
        else:
            end = None

        noteplan = NotePlan(item, start, end, level)
        self._itemplans.append(noteplan)

        avail = self._availspacefor_note(start, end)
        if noteplan.textwidth > avail:
            amount = noteplan.textwidth - avail
            if start:
                start.rpad += amount

            if end:
                end.lpad += amount

    def _calculate_callpaddings(self, itemplan, callee, caller, dir_):
        if itemplan.selfcall:
            callee.rpad = max(callee.rpad, itemplan.textwidth + 3)
        else:
            avail = self._availspacefor_call(
                caller, callee, reverse=dir_ == LEFT
            )
            if itemplan.textwidth > avail:
                amount = itemplan.textwidth - avail
                if dir_ == LEFT:
                    caller.lpad += amount
                else:
                    caller.rpad += amount

    def _plancall(self, item, level):
        caller = self._moduleplans_dict[item.caller]
        callee = self._moduleplans_dict[item.callee]
        diff = self._moduleplans.index(callee) - \
            self._moduleplans.index(caller)

        dir_ = LEFT if diff < 0 else RIGHT
        itemplan = ItemStartPlan(item, caller, callee, dir_, level)
        self._itemplans.append(itemplan)
        self._calculate_callpaddings(itemplan, callee, caller, dir_)

        if len(item):
            self._recurse(item, level + 1)

        itemplan = ItemEndPlan(item, caller, callee, not(dir_), level)
        self._itemplans.append(itemplan)

        if itemplan.text:
            self._calculate_callpaddings(itemplan, callee, caller, dir_)

    def _recurse(self, parent, level):
        for item in parent:
            if isinstance(item, Call):
                self._plancall(item, level)
            elif isinstance(item, (Condition, Loop)):
                self._plancondition(item, level)
            elif isinstance(item, Note):
                self._plannote(item, level)

    def _planitems(self):
        self._itemplans = []
        self._recurse(self.diagram, 0)

    def plan(self):
        self._planmodules()
        self._planitems()

    # Sequence
    def _render_modules(self):
        self._extend(1)
        fm = self._moduleplans[0]
        row = self.row
        col = fm.lpad

        for m, nm in twiniter(self._moduleplans):
            m.drawbox(self, col, row)
            col += m.boxlen + max(m.rpad, nm.lpad if nm else 0)

        if col > self.canvas.cols:
            self.canvas.extendright(col - self.canvas.cols)

    def _render_emptyline(self):
        self._extend(1)
        for m in self._moduleplans:
            m.drawpipe(self, self.row)

        super()._render_emptyline()

    def _render_emptylines(self, count=1):
        for _ in range(count):
            self._render_emptyline()

    def _render_items(self):
        lastdir = None
        lasttype = None

        for c in self._itemplans:
            # Place a blank line if direction was changed.
            if lastdir is not None and (
                    c.direction != lastdir
                    or not lasttype
                    or not isinstance(c, lasttype)):
                self._render_emptylines()

            # Calculte the needed space for the item
            lines_before, lines, lines_after = c.calc()
            self._render_emptylines(lines_before + lines)
            c.draw(self, self.row - (lines - 1))
            self._render_emptylines(lines_after)

            lastdir = c.direction
            lasttype = type(c)

    def render(self):
        self.plan()

        # Sequence Header
        if self.diagram.title:
            self._extend(3)
            self.canvas.write_textline(
                0, self.row, f'SEQUENCE: {self.diagram.title}')

        if self._moduleplans:
            self._extend(1)
            self._render_modules()

        if self._itemplans:
            self._render_emptylines()
            self._render_items()

        if self._moduleplans:
            self._render_emptylines()
            self._render_modules()
