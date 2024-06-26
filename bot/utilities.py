from typing import Tuple, TypeAlias
import math


Point: TypeAlias = Tuple[int, int]
Color: TypeAlias = Tuple[int, int, int]
Rect: TypeAlias = Tuple[int, int, int, int]


def distance_to_point(point_a: Point, point_b: Point) -> float:
    x = abs(point_a[0] - point_b[0])
    y = abs(point_a[1] - point_b[1])    
    return math.sqrt((x*x) + (y*y))


def middle_point(point_a: Point, point_b: Point) -> Point:
    x = (point_a[0] + point_b[0]) / 2
    y = (point_a[1] + point_b[1]) / 2
    return (x, y)


def point_convert_to_int(point: Point) -> Point:
    return int(point[0]), int(point[1])
