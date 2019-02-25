'''
pyscience - python science programming
Copyright (c) 2019 Manuel Alcaraz Zambrano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pyscience, sys, traceback
from pyscience import parser
from pyscience.algebra import get_variables
from pyscience.chemistry.element import ChemicalElement
from pyscience.fraction import Fraction

class PyscienceInterpreter:
    
    def __init__(self):
        self._globals = {}
        
        # Variables
        for variable in get_variables('x y z a b c n m l'):
            self._globals[variable.name] = variable
        
        # Chemical element
        self._globals['CE'] = ChemicalElement
        
        # Fractions
        self._globals['F'] = Fraction
            
    def print_exception(self):
        type, value, tb = sys.exc_info()
        list = traceback.format_tb(tb, None) + traceback.format_exception_only(type, value)
        
        if pyscience.DEBUG:
            print('Traceback (most recent call last):')
            print(''.join(list[:-1]))
        print(list[-1])
        
        del tb
        
    def exec_function(self, cmd):
        func = None
        code = cmd
        
        if ':' in cmd:
            code = cmd[:cmd.index(':')]
            func = cmd[cmd.index(':'):]
            
        try:
            code = parser.expand(code)
        except SyntaxError as e:
            print('SyntaxError:', e)
            return
        
        if func:
            if func.startswith(':for'):
                func = func[4:]
                for val in func.split(','):
                    name, value = val.replace(' ', '').split('=')
                    code = code.replace(name, f'({value})')
        
        if pyscience.DEBUG:
            print(f'eval: "{code}"')
        
        try:
            if code:
                result = eval(code, self._globals)
                if pyscience.DEBUG:
                    print('result type:', type(result))
                    print('result repr:', repr(result))
                print(result)
        except:
            self.print_exception()
