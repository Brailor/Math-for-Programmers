from PIL import Image
from chapter_6 import *
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
# print(ImageVector("melba_face.jpg").image())
# print(0.5 * ImageVector("inside.JPG") + 0.5 * ImageVector("outside.JPG"))

# Exercise 6.39: Write a function solid_color(r,g,b) that returns a solid color ImageVector with the given red, green, and blue content at every pixel
def solid_color(r,g,b):
   return ImageVector([(r,g,b) for _ in range(0,ImageVector.size[0] * ImageVector.size[1])])

# Exercise 6.40−Mini Project: Write a linear map that generates an ImageVector from a 30×30 grayscale image, implemented as a 30×30 matrix of brightness values.
# Then, implement the linear map that takes a 300×300 image to a 30×30 grayscale image by averaging the brightness (average of red, green, and blue) at each pixel.
image_size = (300,300)
total_pixels = image_size[0] * image_size[1]
square_count = 30
square_width = 10

# TODO: investigate
# def from_lowres_grayscale(input_image):
#     dimension = image_size[0]
#     triple = lambda x: (x,x,x)
#     res =[ triple()for y in range(dimension * 10)] 
#     return ImageVector(res)
def from_lowres_grayscale(matrix):
    def lowres(pixels, ij):
        i,j = ij
        return pixels[i // square_width][ j // square_width]
    def make_highres():
        triple = lambda x: (x,x,x)
        return ImageVector([triple(lowres(matrix, ij(n))) for n in range(0,total_pixels)])
    return make_highres(matrix)

def ij(n):
    return (n // image_size[0], n % image_size[1])
 
def to_lowres_grayscale(img):
    matrix = [
        [0 for i in range(0,square_count)]
        for j in range(0,square_count)
    ]
    for (n,p) in enumerate(img.pixels):
        i,j = ij(n)
        weight = 1.0 / (3 * square_width * square_width)
        matrix[i // square_width][ j // square_width] += (sum(p) * weight)
    return matrix
    # return ImageVector()
# img = random_matrix(30,30, 1,3)
# bigger_img = from_lowres_grayscale(img)
print("=====================================================")
# print(f"Ex. 6.40\n\Rows: {len(img)}, cols: {len(img[0])}")
# print(f"\t300x300 rows: {len(bigger_img)}, cols{len(bigger_img[0])}")
# print(f"{img[0][0]} -> {bigger_img[0][2]}")