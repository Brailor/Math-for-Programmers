from typing import *

class Vec2():
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y= y
    def add(self, other: Type[Self]):
        return Vec2(self.x + other.x, self.y + other.y)

v1 = Vec2(1.68,3.4)
v2 = Vec2(3.32,1.6)
sum = v1.add(v2)

print(f"v1 = {(v1.x,v1.y)}, v2 = {(v2.x,v2.y)}. Their sum is = {(sum.x, sum.y)}")