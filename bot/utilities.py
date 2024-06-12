from typing import Tuple, TypeAlias
import math


Point: TypeAlias = Tuple[int, int]
Color: TypeAlias = Tuple[int, int, int]
Rect: TypeAlias = Tuple[int, int, int, int]


def distance_to_point(point_a: Point, point_b: Point) -> float:
    x = abs(point_a[0] - point_b[0])
    y = abs(point_a[1] - point_b[1])    
    return math.sqrt((x*x) + (y*y))


def boxes_intersect(rect_a: Rect, rect_b: Rect) -> bool:
    xa1, ya1, xa2, ya2 = rect_a
    xb1, yb1, xb2, yb2 = rect_b
    
    return not (xa2 < xb1
                or xa1 > xb2
                or ya2 < yb1
                or ya1 > yb2)
