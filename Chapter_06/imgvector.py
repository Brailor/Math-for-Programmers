from PIL import Image
from chapter_6 import Vector
from typing import *

class ImageVector(Vector):
    size = (300,300)

    def __init__(self, input) -> None:
        try:
            img = Image.open(input).resize(ImageVector.size)
            self.pixels = img.getdata()
        except:
            self.pixels = input
    
    def image(self) -> Image:
        img = Image.new("RGB", self.size)
        img.putdata([(int(r), int(g), int(b)) for (r,g,b) in self.pixels])

        return img
    
    def add(self, other: Self) -> Self:
        return ImageVector([(r1+r2, g1+g2, b1+b2) for (r1,g1,b1),(r2,g2,b2) in zip(self.pixels, other.pixels)])
    def scale(self, scalar: int):
        return ImageVector([(r * scalar, g * scalar, b * scalar) for (r,g,b) in self.pixels])
    
    @classmethod
    def zero(cls):
        size = cls.size[0] * cls.size[1]
        return ImageVector(
            tuple(
                (0,0,0) for _ in range(0, size)
                ))
       
    def __repr__(self):
        return f"ImageVector({self.pixels})"
    def __repr_png_(self):
        return self.image()._repr_png_()
print(ImageVector("melba_face.jpg").image())
# print(0.5 * ImageVector("inside.JPG") + 0.5 * ImageVector("outside.JPG"))