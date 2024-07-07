from collections import defaultdict
from time import sleep
from enum import Enum

V_H = 'value hi'
V_0 = 'value 0'
V_1 = 'value 1'
V_2 = 'value 2'
A_B = 'math A+B'
V_F = 'value f'
V_HE = 'value hello'
G_R = 'globalr A'


class Example(Enum):
    SHORTEST_LOOP =      [V_H, 'print']
    END =                [V_0, 'jump']
    DEFINE =             ['value name', 'define', V_0, 'defined', V_0, 'jump']
    MATH_ORDER =         [V_1, V_2, 'value 3', 'math A+B+C', 'print', V_0, 'jump']
    NAMING_LITERAL =     ['value hi how are you', 'define', V_0, 'defined', V_0, 'jump']
    NAMING_MATH =        [V_1, V_2, A_B, 'define', V_0, 'defined', V_0, 'jump']
    NAMING_INPUT =       ['input', 'define', V_0, 'defined', V_0, 'jump']
    UNDEFINED =          [V_H, 'call', V_H, 'define', V_H, 'print', 'defined', V_H, 'call', V_0, 'jump']
    RECURSION_SELF =     [V_F, 'define', V_H, 'print', V_F, 'call', 'defined', V_F, 'call', V_0, 'jump']
    RECURSION_DOUBLE =   [V_H, 'define', V_H, 'print', V_HE, 'call', 'defined', V_HE, 'define', V_HE,
                          'print', V_H, 'call', 'defined', V_H, 'call', V_0, 'jump']
    CALL =               ['value 3', 'define', V_0, 'defined', V_1, V_2, A_B, 'call', V_0, 'jump']
    LOOKBEHIND =         [V_1, V_2, A_B, 'value line 1', 'value line 2', 'value line 3', 'value line 4',
                          'value line 5', 'value line 6', 'value line 7', 'value line 8',
                          'value line 9', 'value line 10', 'math K', 'print', V_0, 'jump']
    CONDITIONAL_JUMPS =  ['value loop', 'define', V_H, 'print', 'globalr', 'math A+1', 'globalw', 'defined',
                          'value loop', 'call', 'globalr', 'math A>3',
                          'math (A==0) * 5 + (A!=0) * (-1)', 'jump', V_0, 'jump']
    TRUTH_MACHINE =      [V_1, 'define', V_1, 'print', V_1, 'call', 'defined',
                          'input', 'call', V_0, 'print', V_0, 'jump']
    COLLATZ_CONJECTURE = ['value step', 'define', 'globalr', 'math A%2 * (3*A+1) + (A%2==0) * A/2', 'globalw',
                          'globalr', 'print', 'defined', 'value enter an arbitrary integer', 'print', 'input',
                          'globalw', 'globalr', 'print', 'math (B!=1) * (-1) + (B==1) * (-3)', 'jump', 'value step',
                          'call', 'globalr', 'math (A!=1) * 4 + (A==1) * (-1)', 'jump', V_0, 'jump']
    EXT_GLOBALW =        [V_H, 'globalw hello', 'globalr hello', V_0, 'jump']
    EXT_GLOBALR =        [V_H, 'globalw', 'globalr', 'globalr _global', V_0, 'jump']
    EXT_CALL_VARIABLES = [V_H, 'globalw hello', V_HE, 'define', G_R, 'print',
                          'defined', V_HE, 'call A', G_R, 'print', V_0, 'jump']
    EXT_CALL_CONTEXT =   [V_HE, 'define', V_H, 'globalw A', G_R, 'print', 'defined', V_H, V_HE, 'call B', V_0, 'jump']


class Interpreter:
    functions: dict
    variables: dict
    exec: list
    extended_features: bool
    verbose: bool
    alphabet: str
    _sleep: float
    _end: bool

    __slots__ = ('functions', 'variables', 'exec', '_sleep', 'extended_features', 'verbose', 'alphabet', '_end')

    def __init__(
            self,
            program: list | None = None,
            extended_features: bool = False,
            verbose: bool = False,
            alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            _sleep: float = 0.1
            ) -> None:
        self.extended_features = extended_features
        self.verbose = verbose
        self.alphabet = alphabet
        self._sleep = _sleep
        self._end = False
        self.functions = {}
        self.variables = {'_global': {'_global': 0}, '_main': defaultdict(int)}
        self.exec = [['_main', 0]]
        if program is None:
            program = self.input_commands()
        elif program:
            print(program)
        else:
            print('Exception while setting up the interpreter')
            print('Length of program must be non-zero')
            self._end = True
        self.functions['_main'] = program

    @staticmethod
    def input_commands() -> list:
        print('Input the While(true){ code separated by colons or newlines, empty line for end of input')
        print('Uses eval() in MATH commands, sanitize input (all letters are replaced, so should be pretty safe)')
        cmd_list = []
        while (line := input().strip().split(';'))[0] != '':
            for cmd in (i.strip() for i in line if i.strip()):
                cmd_list.append(cmd)
        return cmd_list

    def loop(self) -> None:
        while not self._end:
            self.step()

    def _parse_call(self, fn, fp, fc, i) -> bool:
        if not self.extended_features and i:
            print('Exception while handling syntax in CALL')
            print('Extended features not enabled, CALL does not take arguments')
            self._end = True
            return True
        fnname = self.variables[fn][(fp - 1) % len(fc)]
        val = ' '.join(i)
        inx = 0
        for i, v in enumerate(i for i in self.alphabet if i in val):
            self.variables[fnname][self.alphabet[inx]] = self.variables[fn][(fp - 1 - i) % len(fc)]
            inx += 1
        if fnname in self.functions:
            if fnname in (k := (i[0] for i in self.exec)):
                for i, v in enumerate(k):
                    if v == fnname:
                        self.exec = self.exec[:i]
                        break
            self.exec[-1][1] += 1
            if self.exec[-1][1] >= len(self.functions[fn]):
                self.exec[-1][1] = 0
                if fn != '_main':
                    self.exec.pop()
            self.exec.append([fnname, 0])
        return False

    def _parse_define(self, fn, fp, fc) -> bool:
        if fc[fp] == 'defined':
            pass
        else:
            inx = (fp - 1) % len(fc)
            if not self.extended_features and self.variables[fn][inx] in self.functions:
                print('Exception while handling syntax in DEFINE')
                print('Overwriting functions is not enabled')
                self._end = True
                return True
            self.functions[self.variables[fn][inx]] = []
            self.variables[self.variables[fn][inx]] = defaultdict(int)
            while True:
                fp = (fp + 1) % len(fc)
                if self.verbose:
                    print('  ' + fc[fp])
                if fc[fp] == 'defined':
                    break
                self.functions[self.variables[fn][inx]].append(fc[fp])
            if not len(self.functions[self.variables[fn][inx]]):
                print('Exception while handling syntax in DEFINE')
                print('Functions may not be length 0')
                self._end = True
                return True
            self.exec[-1][1] = fp % len(fc)
        return False

    def _parse_globalw(self, fn, fp, fc, i) -> bool:
        if not self.extended_features and i:
            print('Exception while handling syntax in GLOBALW')
            print('Extended features not enabled, GLOBALW does not take arguments')
            self._end = True
            return True
        v = self.variables[fn][(fp - 1) % len(fc)]
        try:
            v = int(v)
        except ValueError:
            v = str(v)
        k = i[0] if len(i) > 0 and i[0] else '_global'
        if k in self.variables[fn]:
            self.variables[fn][k] = v
        else:
            self.variables['_global'][k] = v
        return False

    def _parse_globalr(self, fn, fp, i) -> bool:
        if not self.extended_features and i:
            print('Exception while handling syntax in GLOBALR')
            print('Extended features not enabled, GLOBALR does not take arguments')
            self._end = True
            return True
        access = i[0] if len(i) > 0 and i[0] else '_global'
        if access in self.variables[fn]:
            self.variables[fn][fp] = self.variables[fn][access]
        else:
            self.variables[fn][fp] = self.variables['_global'][access]
        return False

    def _parse_input(self, fn, fp):
        v = input(': ')
        try:
            v = int(v)
        except ValueError:
            v = str(v)
        self.variables[fn][fp] = v or 0

    def _parse_jump(self, fn, fp, fc) -> bool:
        j = int(self.variables[fn][(fp - 1) % len(fc)])
        if not j:
            self._end = True
            return True
        self.exec[-1][1] = (fp - j - 1) % len(fc)
        return False

    def _parse_math(self, fn, fp, fc, i):
        equation = ' '.join(i).upper()
        for i, v in enumerate(self.alphabet):
            if self.extended_features and v in self.variables[fn]:
                equation = equation.replace(v, str(self.variables[fn][v]))
            else:
                equation = equation.replace(v, str(self.variables[fn][(fp - 1 - i) % len(fc)]))
            equation = equation.replace('False', '0')
            equation = equation.replace('True', '1')
        self.variables[fn][fp] = str(int(eval(equation)))

    def _parse_value(self, fn, fp, i):
        v = ' '.join(i)
        try:
            v = int(v)
        except ValueError:
            pass
        self.variables[fn][fp] = v

    def step(self) -> None:
        fn, fp = self.exec[-1]
        fc = self.functions[fn]
        if self.verbose:
            print('' if fn == '_main' else '  ', end='')
            print(fc[fp])
        match fc[fp].split(' '):
            case ['call', *i]:
                if self._parse_call(fn, fp, fc, i):
                    return
            case ['define' | 'defined']:
                if self._parse_define(fn, fp, fc):
                    return
            case ['globalw', *i]:
                if self._parse_globalw(fn, fp, fc, i):
                    return
            case ['globalr', *i]:
                if self._parse_globalr(fn, fp, i):
                    return
            case ['input']:
                self._parse_input(fn, fp)
            case ['jump']:
                if self._parse_jump(fn, fp, fc):
                    return
            case ['math', *i]:
                self._parse_math(fn, fp, fc, i)
            case ['print']:
                print('; '+str(self.variables[fn][(fp - 1) % len(fc)]))
            case ['value', *i]:
                self._parse_value(fn, fp, i)
            case _:
                print('Exception while handling syntax')
                print(f'Unknown command/parameter: {fc[fp]}')
                self._end = True
                return
        self.exec[-1][1] += 1
        if fp + 1 >= len(self.functions[fn]):
            self.exec[-1][1] = 0
            if not fn == '_main':
                self.exec.pop()
        sleep(self._sleep)


if __name__ == '__main__':
    Interpreter().loop()
