from math import sin
from typing import *
from abc import ABCMeta, abstractmethod

# Exercise 10.9: Write a function contains(expression, variable) that checks whether the given expression contains any occurrence of the specified variable
def contains(expression, variable):
    return variable in distinct_variables(expression)


def f(x):
    return (3 * x ** 2 + x) * sin(x)
def pack(maybe_expr):
    if isinstance(maybe_expr, Expression):
        return maybe_expr
    
    if isinstance(maybe_expr, int) or isinstance(maybe_expr, float):
        return Number(maybe_expr)
        
    raise ValueError(f"can't convert {maybe_expr} to expression.")

def distinct_variables(maybe_variable):
    distinct_vars = set()

    def aux(maybe_var, res):
        if isinstance(maybe_var, Variable):
            res.add(maybe_var.symbol)
        elif isinstance(maybe_var, Sum):
            for exp in maybe_var.exps:
                aux(exp, res)
        elif isinstance(maybe_var, Power):
            aux(maybe_var.exponent, res)
            aux(maybe_var.base, res)
        elif isinstance(maybe_var, Product):
            aux(maybe_var.expr1, res)
            aux(maybe_var.expr2, res)
        elif isinstance(maybe_var, Apply):
            aux(maybe_var.argument, res)
        elif isinstance(maybe_var, Quotient):
            aux(maybe_var.denominator, res)
            aux(maybe_var.numerator, res)
        elif isinstance(maybe_var, Difference):
            aux(maybe_var.expr1, res)
            aux(maybe_var.expr2, res)
        elif isinstance(maybe_var, Negative):
            aux(maybe_var.expr, res)


        return res

    
    return aux(maybe_variable, distinct_vars)


# Exercise 10.8−Mini Project: Create an abstract base class called Expression and make all of the elements and combinators inherit from it.
# For instance, class Variable() would become class Variable(Expression).
# Then overload the Python arithmetic operations +, -, *, and / so that they produce Expression objects.
# For instance, the code 2*Variable("x")+3 should yield Sum(Product(Number(2),Variable("x")),Number(3)).

class Expression(metaclass = ABCMeta):
    @abstractmethod
    def expand(self):
        pass
    @abstractmethod
    def evaluate(self, **bindings):
        pass
    def __add__(self, other) -> Self:
        return Sum(self, pack(other))
    def __mul__(self, other):
        return Product(self, pack(other))
    def __sub__(self, other):
        return Difference(self, pack(other))
    def __div__(self, other):
        return Quotient(self, pack(other))
    def __rmul__(self,other):
        return Product(pack(other),self)
    def __truediv__(self,other):
        return Quotient(self,pack(other))
    def __pow__(self,other):
        return Power(self,pack(other))

    
class Number(Expression):
    def __init__(self, number) -> None:
        self.number = number
    def evaluate(self, **bindings):
        return self.number
    def expand(self):
        return self

class Sum(Expression):
    # 5 + A(x + y) => 5 + Ax + Ay
    def expand(self):
        return Sum(*[exp.expand() for exp in self.exps])
    def evaluate(self, **bindings):
        return sum(*[exp.evaluate(**bindings) for exp in self.exps])
    def __init__(self, *exps):
        self.exps = exps

class Power(Expression):
    def expand(self):
        return super().expand()
    def evaluate(self, **bindings):
        return super().evaluate(**bindings)
    def __init__(self, base, exponent) -> None:
        self.base = base
        self.exponent = exponent

class Variable(Expression):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
    def expand(self):
        return self
    def evaluate(self, **bindings):
        try:
            return bindings[self.symbol]
        except:
            return KeyError(f"Variable {self.symbol} is not bound.")

class Product(Expression):
    def __init__(self, expr1: Expression, expr2: Expression) -> None:
        self.expr1 = expr1
        self.expr2 = expr2
    
    def expand(self):
        expanded1 = self.expr1.expand()
        expanded2 = self.expr2.expand()

        if isinstance(expanded1, Sum):
            return Sum(*[Product(e, expanded2).expand() for e in expanded1.exps])
        if isinstance(expanded2, Sum):
            return Sum(*[Product(e, expanded1) for e in expanded2.exps])
        
        return Product(expanded1, expanded2)

    def evaluate(self, **bindings):
        return self.expr1.evaluate(**bindings) * self.expr2.evaluate(**bindings)


class Function():
    def evaluate(self, **bindings):
        return super().evaluate(**bindings)
    def expand(self):
        return super().expand()
    def __init__(self,name):
        self.name = name

class Apply(Expression):
    def __init__(self,function,argument):
        self.function = function
        self.argument = argument

    def evaluate(self, **bindings):
        return super().evaluate(**bindings)
    def expand(self):
        return Apply(self.function, self.argument.expand())

# Exercise 10.4: Implement a Quotient combinator representing one expression divided by another. How do you represent the following expression?
class Quotient(Expression):
    def evaluate(self, **bindings):
        return super().evaluate(**bindings)
    def expand(self):
        return super().expand()
    def __init__(self, numerator, denominator) -> None:
        self.numerator = numerator
        self.denominator = denominator

class Difference(Expression):
    def evaluate(self, **bindings):
        return super().evaluate(**bindings)
    def expand(self):
        return super().expand()
    def __init__(self, expr1, expr2) -> None:
        self.expr1 = expr1
        self.expr2 = expr2

class Negative(Expression):
    def evaluate(self, **bindings):
        return super().evaluate(**bindings)
    def expand(self):
        return super().expand()
    def __init__(self, expr) -> None:
        self.expr = expr

