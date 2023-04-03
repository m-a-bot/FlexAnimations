import numpy
from PIL import Image, ImageDraw


def get_barycentric_coords(point, v0, v1, v2):
    T = numpy.zeros((3, 3))
    T[:2, 0] = v0
    T[:2, 1] = v1
    T[:2, 2] = v2
    T[-1, :] = numpy.array([1, 1, 1])

    X = numpy.array([point[0], point[1], 1], dtype=numpy.float64).T

    return numpy.linalg.inv(T) @ X


def get_triangle(width, height, color):

    img = numpy.zeros((width, height, 4), dtype=numpy.uint8)
    img[:,:,3] = 0

    point1 = (0,0)
    point2 = (width/2, height)
    point3 = (width, 0)

    for w in range(0, width):
        for h in range(0, height):

            a, b, c = get_barycentric_coords([w,h], point1, point2, point3)

            if a >= 0 and b >= 0 and c >= 0:
                img[w,h,:3] = color
                img[w,h, 3] = 255

    return Image.fromarray(img, mode="RGBA")

def get_rectangle_gradient(width, height, color1, color2, vert=True):

    img = numpy.zeros((width, height, 4), dtype=numpy.uint8)
    img[:,:,3]=255
    colors = numpy.round(numpy.linspace(color1, color2, width)) if vert else numpy.round(numpy.linspace(color1, color2, height))

    for x in range(0, width):
        for y in range(0, height):
            img[x, y, :3] = colors[x if vert else y]

    return Image.fromarray(img, mode="RGBA")


def get_triangle_random(width, height):

    img = numpy.zeros((width, height, 4), dtype=numpy.uint8)
    img[:,:,3] = 0

    point1 = (0,0)
    point2 = (width/2, height)
    point3 = (width, 0)

    for w in range(0, width):
        for h in range(0, height):

            a, b, c = get_barycentric_coords([w,h], point1, point2, point3)

            if a >= 0 and b >= 0 and c >= 0:
                img[w,h,:3] = (int(a * 255), int(b * 255), int(c * 255))
                img[w,h, 3] = 255

    return Image.fromarray(img, mode="RGBA")


