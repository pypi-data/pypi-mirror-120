from functools import cached_property
from typing import NamedTuple
import abc

from htmlclasses import E


class Point(NamedTuple):

    x: float
    y: float

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)


class BoundingBox(NamedTuple):
    """...

        Parameters
        ----------
        llc: lower left corner
        urc: upper right corner
    """
    llc: Point
    urc: Point

    @classmethod
    def from_points(cls, points):
        xs, ys = zip(*points)
        return cls(Point(min(xs), min(ys)), Point(max(xs), max(ys)))


class Drawable(abc.ABC):

    @cached_property
    def span_x(self):
        (x_min, y_min), (x_max, y_max) = self.bbox
        return x_max - x_min

    @cached_property
    def span_y(self):
        (x_min, y_min), (x_max, y_max) = self.bbox
        return y_max - y_min

    @property
    @abc.abstractmethod
    def bbox(self):
        pass


class Line(Drawable):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'Line(start={self.start}, end={self.end})'

    def __iter__(self):
        return iter((self.start, self.end))

    @property
    def bbox(self):
        return BoundingBox.from_points(self)


class DataPoints(Drawable):

    def __init__(self, *, points, bbox):
        self._points = points
        self._bbox = bbox

    @cached_property
    def points(self):
        p_xs, p_ys = zip(*self._points)
        p_span_x = max(p_xs) - (p_xs_min := min(p_xs))
        p_span_y = max(p_ys) - (p_ys_min := min(p_ys))

        drawable_span_x = self.span_x
        drawable_span_y = self.span_y
        drawable_llc = self.bbox.llc

        def map_data_point_to_drawable_point(point):
            x, y = point
            p_x_ratio = (x - p_xs_min) / p_span_x
            p_y_ratio = (y - p_ys_min) / p_span_y
            drawable = drawable_llc + Point(
                    p_x_ratio * drawable_span_x,
                    p_y_ratio * drawable_span_y,
                    )
            return drawable

        def _iter():
            for point in self._points:
                yield map_data_point_to_drawable_point(point)

        return list(_iter())

    @property
    def bbox(self):
        return self._bbox


class Text(Drawable):

    bbox = NotImplemented

    def __init__(self, *, anchor, text, width, height, font_family):
        self.anchor = anchor
        self.text = text
        self.font_family = font_family
        self.height = height
        self.width = width


def transform_to_svg(element):
    (x_offset, _), (_, y_offset) = element.bbox

    def map_point(point):
        x, y = point
        new_x = x - x_offset
        new_y = y_offset - y
        return Point(new_x, new_y)

    def make_svg_elem(elem):

        if isinstance(elem, Drawable):

            if isinstance(elem, Line):

                class line(E):
                    x1, y1 = map_point(elem.start)
                    x2, y2 = map_point(elem.end)
                    stroke = 'black'

                return line

            elif isinstance(elem, DataPoints):

                class polyline(E):
                    points = ' '.join(
                            f'{",".join(map(str, map_point(p)))}'
                            for p in elem.points
                            )
                    stroke = 'black'
                    fill = 'none'

                return polyline
            elif isinstance(elem, Text):

                class text(E):
                    TEXT = elem.text
                    x, y = map_point(elem.anchor)
                    textLength = f'{elem.width}px'
                    lengthAdjust = 'spacingAndGlyphs'

                    style = (
                            f'font-family: {elem.font_family};'
                            + f' font-size: {elem.height}px;'
                    )

                return text

            else:
                1 / 0

        else:

            class g(E):
                name = type(elem).__name__
                for _subelem in elem.elements:
                    subelement = make_svg_elem(_subelem)

            return g

    g = make_svg_elem(element)

    return g
