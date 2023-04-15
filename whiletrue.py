from time import sleep
from typing import Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Example:
    INFINITE_LOOP =      ['value hi', 'print']
    END =                ['value 0', 'jump']
    DEFINE =             ['value name', 'define', 'value 0', 'defined', 'value 0', 'jump']
    MATH_ORDER =         ['value 1', 'value 2', 'value 3', 'math A+B+C', 'print', 'value 0', 'jump']
    NAMING_LITERAL =     ['value hi how are you', 'define', 'value 0', 'defined', 'value 0', 'jump']
    NAMING_MATH =        ['value 1', 'value 2', 'math A+B', 'define', 'value 0', 'defined', 'value 0', 'jump']
    NAMING_INPUT =       ['input', 'define', 'value 0', 'defined', 'value 0', 'jump']
    UNDEFINED =          ['value hi', 'call', 'value hi', 'define', 'value hi', 'print', 'defined', 'value hi', 'call',
                          'value 0', 'jump']
    RECURSION_SELF =     ['value hi', 'define', 'value hi', 'print', 'value hi', 'call', 'defined', 'value hi', 'call',
                          'value 0', 'jump']
    RECURSION_DOUBLE =   ['value hi', 'define', 'value hi', 'print', 'value hello', 'call', 'defined', 'value hello',
                          'define', 'value hello', 'print', 'value hi', 'call', 'defined', 'value hi', 'call',
                          'value 0', 'jump']
    CALL =               ['value 3', 'define', 'value 0', 'defined', 'value 1', 'value 2', 'math A+B', 'call',
                          'value 0', 'jump']
    LOOKBEHIND =         ['value 1', 'value 2', 'math A+B', 'value line 1', 'value line 2', 'value line 3',
                          'value line 4', 'value line 5', 'value line 6', 'value line 7', 'value line 8',
                          'value line 9', 'value line 10', 'math K', 'print', 'value 0', 'jump']
    CONDITIONAL_JUMPS =  ['value loop', 'define', 'value hi', 'print', 'globalr', 'math A+1', 'globalw', 'defined',
                          'value loop', 'call', 'globalr', 'math A>3', 'math (A==0) * 5 + (A!=0) * (-1)', 'jump',
                          'value 0', 'jump']
    TRUTH_MACHINE =      ['value 1', 'define', 'value 1', 'print', 'value 1', 'call', 'defined', 'input', 'call',
                          'value 0', 'print', 'value 0', 'jump']
    COLLATZ_CONJECTURE = ['value step', 'define', 'globalr', 'math A%2 * (3*A+1) + (A%2==0) * A/2', 'globalw',
                          'globalr', 'print', 'defined', 'value enter an arbitrary integer', 'print', 'input',
                          'globalw', 'globalr', 'print', 'math (B!=1) * (-1) + (B==1) * (-3)', 'jump', 'value step',
                          'call', 'globalr', 'math (A!=1) * 4 + (A==1) * (-1)', 'jump', 'value 0', 'jump']
    EXT_GLOBALW =        ['value hi', 'globalw hello', 'globalr hello', 'value 0', 'jump']
    EXT_GLOBALR =        ['value hi', 'globalw', 'globalr', 'globalr _global', 'value 0', 'jump']
    EXT_CALL_VARIABLES = ['value hi', 'globalw hello', 'value hello', 'define', 'globalr A', 'print', 'defined',
                          'value hello', 'call A', 'globalr A', 'print', 'value 0', 'jump']
    EXT_CALL_CONTEXT =   ['value hello', 'define', 'value hi', 'globalw A', 'globalr A', 'print', 'defined', 'value hi',
                          'value hello', 'call B', 'value 0', 'jump']


@dataclass
class Interpreter:
    functions: dict
    variables: dict
    exec: list
    extended_features: bool
    verbose: bool
    alphabet: str
    end: bool

    def __init__(
            self,
            program: Optional[list] = None,
            extended_features: bool = False,
            verbose: bool = False,
            sleep: float = 0,
            alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            ) -> None:
        self.extended_features = extended_features
        self.verbose = verbose
        self.sleep = sleep
        self.alphabet = alphabet
        self.end = False
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
            self.end = True
        self.functions['_main'] = program

    @staticmethod
    def input_commands() -> list:
        print('Input the While(true){ code separated by colons or newlines, empty line for end of input')
        print('Uses eval() in MATH commands, make sure to sanitize it (all letters are replaced, so should be pretty safe)')
        cmd_list = []
        while (line := input().strip().split(';'))[0] != '':
            for cmd in (i.strip() for i in line if i.strip()):
                cmd_list.append(cmd)
        return cmd_list

    def loop(self) -> None:
        while not self.end:
            self.step()

    def step(self) -> None:
        fn, fp = self.exec[-1]
        fc = self.functions[fn]
        if self.verbose:
            print('' if fn == '_main' else '  ', end='')
            print(fc[fp])
        match fc[fp].split(' '):
            case ['call', *i]:
                if not self.extended_features and i:
                    print('Exception while handling syntax in CALL')
                    print('Extended features not enabled, CALL does not take arguments')
                    self.end = True
                    return
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
                        if not fn == '_main':
                            self.exec.pop()
                    self.exec.append([fnname, 0])
                    return
            case ['define' | 'defined']:
                if fc[fp] == 'defined':
                    pass
                else:
                    inx = (fp - 1) % len(fc)
                    if not self.extended_features and self.variables[fn][inx] in self.functions:
                        print('Exception while handling syntax in DEFINE')
                        print('Overwriting functions is not enabled')
                        self.end = True
                        return
                    self.functions[self.variables[fn][inx]] = []
                    self.variables[self.variables[fn][inx]] = defaultdict(int)
                    while True:
                        fp = (fp + 1) % len(fc)
                        if self.verbose:
                            print('  '+fc[fp])
                        if fc[fp] == 'defined':
                            break
                        self.functions[self.variables[fn][inx]].append(fc[fp])
                    if not len(self.functions[self.variables[fn][inx]]):
                        print('Exception while handling syntax in DEFINE')
                        print('Functions may not be length 0')
                        self.end = True
                        return
                    self.exec[-1][1] = fp % len(fc)
            case ['globalw', *i]:
                if not self.extended_features and i:
                    print('Exception while handling syntax in GLOBALW')
                    print('Extended features not enabled, GLOBALW does not take arguments')
                    self.end = True
                    return
                v = self.variables[fn][(fp - 1) % len(fc)]
                try:
                    v = int(v)
                except ValueError:
                    v = str(v)
                k = i[0] if len(i) > 0 and i[0] else '_global'
                if k in self.variables[fn].keys():
                    self.variables[fn][k] = v
                else:
                    self.variables['_global'][k] = v
            case ['globalr', *i]:
                if not self.extended_features and i:
                    print('Exception while handling syntax in GLOBALR')
                    print('Extended features not enabled, GLOBALR does not take arguments')
                    self.end = True
                    return
                access = i[0] if len(i) > 0 and i[0] else '_global'
                if access in self.variables[fn].keys():
                    self.variables[fn][fp] = self.variables[fn][access]
                else:
                    self.variables[fn][fp] = self.variables['_global'][access]
            case ['input']:
                v = input(': ')
                try:
                    v = int(v)
                except ValueError:
                    v = str(v)
                self.variables[fn][fp] = v
            case ['jump']:
                j = int(self.variables[fn][(fp - 1) % len(fc)])
                if not j:
                    self.end = True
                    return
                self.exec[-1][1] = (fp - j - 1) % len(fc)
            case ['math', *i]:
                equation = ' '.join(i).upper()
                for i, v in enumerate(self.alphabet):
                    if self.extended_features and v in self.variables[fn].keys():
                        equation = equation.replace(v, str(self.variables[fn][v]))
                    else:
                        equation = equation.replace(v, str(self.variables[fn][(fp - 1 - i) % len(fc)]))
                    equation = equation.replace('False', '0')
                    equation = equation.replace('True', '1')
                self.variables[fn][fp] = str(int(eval(equation)))
            case ['print']:
                print('; '+str(self.variables[fn][(fp - 1) % len(fc)]))
            case ['value', *i]:
                v = ' '.join(i)
                try:
                    v = int(v)
                except ValueError:
                    pass
                self.variables[fn][fp] = v
            case _:
                print('Exception while handling syntax')
                print(f'Unknown command/parameter: {fc[fp]}')
                self.end = True
                return
        self.exec[-1][1] += 1
        if fp + 1 >= len(self.functions[fn]):
            self.exec[-1][1] = 0
            if not fn == '_main':
                self.exec.pop()
        sleep(self.sleep)


if __name__ == '__main__':
    Interpreter().loop()
