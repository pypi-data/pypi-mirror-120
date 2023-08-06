from decimal import Decimal, InvalidOperation
from importlib import import_module
import unicodedata

from .lib import CalcError

class Env:

    def __init__(self, prelude=True):
        self.stack = []
        self.history = [[]]
        self.max_history = 10
        self.ops = {}
        self.stacks = {}
        self.vals = {}
        self.error = None
        self.output = None
        self.use('builtin')
        if prelude:
            self.use('bit')
            self.use('math')
            self.use('sci')

    def eval(self, line):
        self.error = None
        entries = parse_line(line)
        if len(entries) == 0:
            if self.output:
                self.output = None
                return
            if len(self.stack) > 0:
                self.stack.pop()
                return
        self.output = None
        for entry in entries:
            self._eval_entry(entry)
            if self.error:
                return

    def do(self, line):
        self.eval(line)
        if len(self.history) == 0 or self.stack != self.history[-1]:
            self.history.append(self.stack.copy())
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def run(self):
        if len(self.stack) == 0:
            return
        line = self.pop()
        self.eval(line)

    def _eval_entry(self, entry):
        try:
            first = entry[0] if len(entry) > 0 else ''
            if first == '[':
                return self._eval_inline_fn(entry)
            elif first == '"' or first == "'":
                self.stack.append(entry[1:])
            elif not self._eval_op(entry):
                self.stack.append(entry.strip())
        except CalcError as e:
            self.error = e

    def _eval_inline_fn(self, line):
        parts = parse_inline_fn(line[1:])
        fn = parts[0]
        args = parts[1:]
        for arg in args:
            self.stack.append(arg)
        self._eval_entry(fn)

    def _eval_op(self, name):
        name = name.strip()
        op = self.ops.get(name)
        if not op:
            return False
        op(self)
        return True

    def use(self, name):
        try:
            mod = import_module(f'zcalc.stdlib.{name}')
        except ModuleNotFoundError:
            try:
                mod = import_module(name)
            except ModuleNotFoundError:
                raise CalcError(f'no such module: {name}')
        for export in dir(mod):
            obj = getattr(mod, export)
            if not hasattr(obj, 'zcalc_name'):
                continue
            self.ops[obj.zcalc_name] = obj
            for alias in obj.zcalc_aliases:
                self.ops[alias] = obj

    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            raise CalcError('stack empty')

    def pop_float(self):
        return parse_float(self.pop())

    def pop_decimal(self):
        return parse_decimal(self.pop())

    def pop_int(self):
        return parse_int(self.pop())

    def pop_number(self):
        n = self.pop()
        parsers = [
            parse_decimal,
            parse_int,
        ]
        for parse in parsers:
            try:
                return parse(n)
            except CalcError:
                pass
        raise CalcError(f'not a number: ${n}')

    def push(self, v):
        self.stack.append(str(v))

    def binary_op(self, pop, push, op):
        b = pop()
        a = pop()
        return push(op(a, b))

    def unary_op(self, pop, push, op):
        a = pop()
        return push(op(a))

    def op2(self, op, pop=None, push=None):
        pop = pop if pop is not None else self.pop
        push = push if push is not None else self.push
        b = pop()
        a = pop()
        return push(op(a, b))

    def op1(self, op, pop=None, push=None):
        pop = pop if pop is not None else self.pop
        push = push if push is not None else self.push
        a = pop()
        return push(op(a))

    def get_stack(self):
        name = self.pop()
        try:
            return self.stacks[name]
        except KeyError:
            raise CalcError(f'no such stack: {name}')

def _clean_numeric(dirty):
    clean = []
    for char in dirty:
        if char == ',':
            continue
        if unicodedata.category(char) == 'Sc': # symbol, currency
            continue
        clean.append(char)
    return ''.join(clean)


def parse_int(n):
    try:
        return int(_clean_numeric(n), 0)
    except ValueError:
        raise CalcError(f'not an integer: {n}')


def parse_decimal(n):
    try:
        return Decimal(_clean_numeric(n))
    except ValueError:
        raise CalcError(f'not a decimal: {n}')
    except InvalidOperation:
        raise CalcError(f'not a decimal: {n}')

def parse_float(n):
    try:
        return float(_clean_numeric(n))
    except ValueError:
        raise CalcError(f'not a float: ${n}')


def parse_line(line):
    entries = []
    entry = []
    for char in line:
        if char.isspace() and len(entry) == 0:
            continue
        if char == ';':
            entries.append(''.join(entry))
            entry = []
            continue
        entry.append(char)
    if len(entry) > 0:
        entries.append(''.join(entry))
    return entries

def parse_inline_fn(line):
    args = []
    arg = []
    quote = None
    for char in line:
        if not quote and char.isspace() and len(arg) > 0:
            args.append(''.join(arg))
            arg = []
            continue
        if not quote and char.isspace():
            continue
        if not quote and (char == "'" or char == '"'):
            quote = char
            arg.append(char)
            continue
        if quote and char == quote:
            quote = None
            continue
        arg.append(char)
    if len(arg) > 0:
        args.append(''.join(arg))
    return args