from typing import *
from abc import ABCMeta, abstractmethod
from typing import Any
from vectors import add, scale
from math import isclose,sin
from datetime import datetime

from json import loads, dumps
from pathlib import Path
from datetime import datetime
from plot import plot

contents = Path('cargraph.json').read_text()
cg = loads(contents)
cleaned = []

def parse_date(s):
    input_format="%m/%d - %H:%M"
    return datetime.strptime(s,input_format).replace(year=2018)
class Vector(metaclass = ABCMeta):
    @abstractmethod
    def scale(self, scalar:int):
        pass
    @abstractmethod
    def add(self, other):
        pass
    @abstractmethod
    def zero(self):
        pass
    def __add__(self, other: Type[Self]) -> Self:
        return self.add(other)
    def __mul__(self, scalar: int) -> Self:
        return self.scale(scalar)
    def __rmul__(self, scalar: int) -> Self:
        return self.scale(scalar)
    def __truediv__(self, scalar: float) -> Self:
        assert not isclose(scalar, 0.0)
        return self.scale(1.0/scalar)
    def subtract(self,other):
       return self.add(-1 * other)
    def __sub__(self,other):
       return self.subtract(other)
    def __neg__(self):
        return self.__class__.negate(self)
    def negate(self):
        return self.scale(-1)


# Exercise 6.6: As equality is implemented for Vec2 and Vec3, it turns out that Vec2(1,2) == Vec3(1,2,3) returns True.
# Python’s duck typing is too forgiving for its own good! 
# Fix this by adding a check that classes must match before testing vector equality.
class Vec2(Vector):
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y
    @classmethod
    def zero(self):
        return Vec2(0,0)
    def add(self, other: Type[Self]) -> Self:
        assert isinstance(other, self.__class__)
        return Vec2(self.x + other.x, self.y + other.y)
    def scale(self, scalar: int) -> Self:
        return Vec2(self.x * scalar, self.y * scalar)
    def __eq__(self, other: Self) -> bool:
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x},{self.y})"

v1 = Vec2(1.68,3.4)
v2 = Vec2(3.32,1.6)
sum_vs= v1.add(v2)

print(f"v1 = {v1}, v2 = {v2}. Their sum is = {sum_vs}")
print((v1 * 3), (5 * v2), (v1 + v2))

class Vec3(Vector):
    def __init__(self, x:int, y:int, z:int) -> None:
        self.x = x
        self.y = y
        self.z = z
    def add(self, other: Type[Self]) -> Self:
        assert isinstance(other, self.__class__)
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    def scale(self, scalar: int) -> Self:
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    def __eq__(self, other: Type[Self]) -> bool:
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y and self.z == other.z
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x},{self.y},{self.z})"
    @classmethod
    def zero(self):
        return Vec3(0,0,0)
v3 = Vec3(1,2,3)
v4 = Vec3(1,2,3)
print(v3 * 2, v3 + v3, v3 == v4)

def average(v1,v2):
    return 0.5 * v1 + 0.5 * v2

print(average(Vec2(2,4), Vec2(5,6)))
print(average(Vec3(2,4,5), Vec3(5,6,8)))
print(f"Original: {v3}, negated: {v3.negate()}")
print(f"Original: {v3}, zero-vector: {v3.zero()}")

# Exercise 6.2-Mini Project: Implement a CoordinateVector class inheriting from Vector with an abstract property representing the dimension.
# This should save repetitious work when implementing specific coordinate vector classes.
# Inheriting from CoordinateVector and setting the dimension to 6 should be all you need to do to implement a Vec6 class.

class CoordinateVector(Vector):
    @property
    @abstractmethod
    def dimension(self):
        pass
    def __init__(self, *coordinates) -> None:
        self.coordinates = tuple(coordinate for coordinate in coordinates)
    def add(self, other: Self) -> Self:
        return self.__class__(*add(self.coordinates, other.coordinates))
    def scale(self,scalar):
       return self.__class__(*scale(scalar, self.coordinates))
    def __repr__(self):
       return "{}{}".format(self.__class__.__qualname__, self.coordinates)


class Vec6(CoordinateVector):
    def dimension(self):
        return 6
    @classmethod
    def zero(self):
        return Vec6(0,0,0,0,0,0)
class Vec0(Vector):
    def __init__(self) -> None:
        pass
    def add(self, other):
        return Vec0() 
    def scale(self, other):
        return Vec0() 
    @classmethod
    def zero(cls):
        return Vec0()
    def __eq__(self,other):
        return self.__class__ == other.__class__ == Vec0
    def __repr__(self):
        return "Vec0()"

print(Vec6(1,2,3,4,5,6) + Vec6(1, 2, 3, 4, 5, 6))
print(Vec6(1,2,3,4,5,6).zero())
print(-Vec6(1,2,3,4,5,6))
print(Vec2(1,2) == Vec3(1,2,3))
# print(Vec2(1,2) + Vec3(1,2,3))
print(Vec2(1,2)/0.5)

class CarForSale(Vector):
    retrieved_dt = datetime(2018,11,24,12)
    def __init__(self, model_year, mileage, price, posted_datetime, 
                model="(virtual)", source="(virtual)", location="(virtual)", description="(virtual)"):
       self.model_year = model_year
       self.mileage = mileage
       self.price = price
       self.posted_datetime = posted_datetime
       self.model = model
       self.source = source
       self.location = location
       self.description = description
    
    def add(self, other: Self) -> Self:
        def add_datetimes(d1:datetime, d2:datetime):
            dt1 = CarForSale.retrieved_dt - d1
            dt2 = CarForSale.retrieved_dt - d2
            sum_ages = dt1 + dt2
            return CarForSale.retrieved_dt - sum_ages

        return CarForSale(
            self.model_year + other.model_year,
            self.mileage + other.mileage,
            self.price + other.price,
            add_datetimes(self.posted_datetime, other.posted_datetime)
        )
    def scale(self, scalar: int) -> Self:
        def scale_datetime(d1:datetime, scalar):
            age = CarForSale.retrieved_dt - d1 
            return CarForSale.retrieved_dt - (scalar * age)

        return CarForSale(
            self.model_year * scalar,
            self.mileage * scalar,
            self.price * scalar,
            scale_datetime(self.posted_datetime, scalar)
        )
    def __eq__(self, other: Self) -> bool:
        return isclose(self.model_year, other.model_year) and isclose(self.mileage, other.mileage) and isclose(self.price, other.price)# and isclose(self.posted_datetime,other.posted_datetime)

    @classmethod
    def zero(self):
        return CarForSale(0, 0, 0, CarForSale.retrieved_dt)
    
    def __repr__(self) -> str:
        return f"CarForSale(model_year={self.model_year}, mileage={self.mileage}, price={self.price}, posted_datetime={self.posted_datetime})" 

for car in cg[1:]:
    try:
        row = CarForSale(int(car[1]), float(car[3]), float(car[4]), parse_date(car[6]), car[2],  car[5],  car[7], car[8])
        cleaned.append(row)
    except: pass

cars = cleaned
print((cars[0] + cars[1]).__dict__)

avg_prius = sum(cars, CarForSale.zero()) / len(cars)
print(avg_prius)


class Matrix(Vector):
    @property
    @abstractmethod
    def rows():
        pass

    @property
    @abstractmethod
    def columns():
        pass

    def __init__(self, matrix) -> None:
        self.matrix = matrix
    def add(self, other: Self):
        return self.__class__(
            tuple(
                tuple(a + b for a,b in zip(row1,row2))
                for row1,row2 in zip(self.matrix, other.matrix)
            )
        )
    def scale(self, scalar: int):
        return self.__class__(
            tuple(
                tuple(a * scalar for a in row)
                for row in self.matrix
            )
        )
    @classmethod
    def zero(cls):
        return cls(
            tuple(
                tuple(0 for _ in range(0, cls.columns(cls)))
                for _ in range(0, cls.rows(cls))
            )
        )
    def __repr__(self) -> str:
        return f"Matrix_{self.rows()}_x_{self.columns()}({self.matrix})"

# ((1,2,3),(4,5,6),(7,8,9),(10,11,12),(13,14,15))
# +
# ((1,2,3),(4,5,6),(7,8,9),(10,11,12),(13,14,15))
# ((1 + 1, 2 + 2, 3 + 3)...)
class Matrix_5_x_3(Matrix):
    def rows(self):
        return 5
    def columns(self):
        return 3
    
class Matrix_2_x_5(Matrix):
    def rows(self):
        return 2
    def columns(self):
        return 5

a = ((1,2,3),(4,5,6),(7,8,9),(10,11,12),(13,14,15))
b = ((10,9,8,7,6),(5,4,3,2,1))
print(Matrix_5_x_3.zero())
print(Matrix_5_x_3(a))
print(Matrix_5_x_3(a) + Matrix_5_x_3(a))
print(Matrix_5_x_3(a) * 5)
print(Matrix_2_x_5(b))


# Exercise 6.10: Implement the class Function(Vector) that takes a function of one variable as an argument to its constructor and
# implement a __call__ method so you can treat it as a function.
# You should be able to run plot([f,g,f+g,3*g],−10,10).
class Function(Vector):
    def __init__(self, fn) -> None:
        self.fn = fn
    def add(self, other: Self):
        return Function(lambda x: other(x) + self(x))

    def scale(self, scalar: int):
        return Function(lambda x: self(x) * scalar)
    @classmethod
    def zero(cls):
        return Function(lambda x: 0)
    def __call__(self, *args: Any) -> Any:
        assert len(args) == 1
        
        return self.fn(args[0])

f = Function(lambda x: x + 1)
g = Function(lambda x: x * 2)
f_g = f + g
# print(f + g)
print(f_g(2))
print((f*2)(5))