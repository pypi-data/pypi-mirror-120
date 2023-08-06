import enum

import numpy as np

from . import core


class UnknownPosition(Exception):
    pass


class UnrecognizedPosition(Exception):
    pass


class Position(enum.Enum):

    DOWN = enum.auto()
    LEFT = enum.auto()


class Element:

    @property
    def elements(self):
        raise NotImplementedError()

    @property
    def bbox(self):
        raise NotImplementedError()


class Axis:

    def __init__(self, *, main):
        """
        tail and head are optional
        """
        ticks = ...
        self.elements = [main] + ticks


class LabeledTick:

    _TICK_LENGTH = 10

    def __init__(self, *, label, anchor, position, max_num_chars):
        assert label.num_chars <= max_num_chars  # nosec
        if position == Position.DOWN:
            tick = core.Line(
                    anchor,
                    core.Point(anchor.x, anchor.y - self._TICK_LENGTH))
            text_anchor = tick.end - core.Point(
                    label.width / 2, label.height)
        elif position == Position.LEFT:
            tick = core.Line(
                    anchor,
                    core.Point(anchor.x - self._TICK_LENGTH, anchor.y))
            text_anchor = tick.end - core.Point(label.width, label.height / 2)
        else:
            UnknownPosition(position)
        self._text_anchor = text_anchor
        self._text = core.Text(
                anchor=text_anchor,
                text=label.text,
                font_family=label.font.family,
                width=label.width,
                height=label.height,
                )
        self._anchor = anchor
        self._tick = tick

    @property
    def elements(self):
        return [self._tick, self._text]

    @property
    def bbox(self):
        return core.BoundingBox(
                llc=self._text_anchor,
                urc=core.Point(
                    self._text_anchor.x + self._length,
                    self._anchor.y,
                ),
        )

    @classmethod
    def calculate_width(
            cls,
            *,
            font,
            max_num_chars,
            position,
            ):
        text_width = font.calculate_max_width(max_num_chars)
        if position == Position.DOWN:
            return text_width
        elif position == Position.LEFT:
            return text_width + cls._TICK_LENGTH
        else:
            UnrecognizedPosition(position)

    @classmethod
    def calculate_height(
            cls,
            *,
            font,
            position,
            ):
        if position == Position.DOWN:
            return font.height + cls._TICK_LENGTH
        elif position == Position.LEFT:
            return font.height
        else:
            UnrecognizedPosition(position)


class Title:

    _MARGIN = 5

    def __init__(
            self,
            title,
            width,
            p0,
            ):
        height = self.calculate_height(title.font)
        middle = p0 + core.Point(width / 2, height / 2)
        text_anchor = middle - core.Point(title.width / 2, title.height / 2)
        self.elements = [
            core.Text(
                anchor=text_anchor,
                text=title.text,
                font_family=title.font.family,
                width=title.width,
                height=title.height,
            )
        ]

    @classmethod
    def calculate_height(cls, font):
        return font.height + 2 * cls._MARGIN


class Monospace:

    def __init__(self, *, height):
        self.height = height
        self._width = height * 3 / 5
        self.family = 'monospace'
        self.max_char_width = self._width

    def calculate_min_width(self, num_chars):
        return self._width * num_chars

    def parse(self, text):
        return TextWithFont(text=text, font=self)

    def calculate_width(self, text):
        return len(text) * self._width

    def calculate_max_width(self, max_num_chars):
        return max_num_chars * self._width


class TextWithFont:

    def __init__(self, *, text, font):
        self.text = text
        self.font = font
        self.width = font.calculate_width(text)
        self.height = font.height
        self.num_chars = len(text)


class PositionedPlot2D:

    def __init__(
            self,
            *,
            bbox,
            data_points,
            title,
            ):
        width = bbox.urc.x - bbox.llc.x

        title_font = Monospace(height=30)
        title_height = Title.calculate_height(title_font)

        title_elem = Title(
                title=title_font.parse(title),
                width=width,
                p0=core.Point(
                    bbox.llc.x,
                    bbox.urc.y - title_height,
                ),
        )
        core_area = _Plot2DCore(
            bbox=core.BoundingBox(
                llc=bbox.llc,
                urc=core.Point(bbox.urc.x, bbox.urc.y - title_height),
            ),
            data_points=data_points,
            label_font=Monospace(height=12),
        )
        self.elements = [title_elem, core_area]
        self.bbox = bbox


class Plot2D(PositionedPlot2D):

    def __init__(
            self,
            *,
            width,
            height,
            data_points,
            title,
            ):
        super().__init__(
            bbox=core.BoundingBox(
                llc=core.Point(0, 0),
                urc=core.Point(width, height),
            ),
            data_points=data_points,
            title=title,
        )


class Vector(core.Point):
    pass


class _Plot2DCore:

    def __init__(
            self,
            *,
            bbox,
            data_points,
            label_font,
    ):
        self.bbox = bbox

        horizontal_axis, vertical_axis = self._build_axes(
            bbox=bbox,
            label_font=label_font,
            data=data_points,
        )

        x_min, x_max = horizontal_axis.material_range
        y_min, y_max = vertical_axis.material_range

        data = core.DataPoints(
                points=data_points,
                bbox=core.BoundingBox(
                    llc=core.Point(x_min, y_min),
                    urc=core.Point(x_max, y_max),
                ),
        )

        self.elements = [
            horizontal_axis,
            vertical_axis,
            data,
        ]

    def _build_axes(
            self,
            label_font,
            bbox,
            data,
            ):
        vertical_axis_width = VerticalAxis.calculate_width(font=label_font)
        total_width = bbox.urc.x - bbox.llc.x
        horizontal_axis_length = total_width - 2 * vertical_axis_width
        data_xs, data_ys = zip(*data)
        horizontal_axis = HorizontalAxis(
            label_font=label_font,
            data_range=(min(data_xs), max(data_xs)),
            p0=bbox.llc + core.Point(vertical_axis_width, 0),
            length=horizontal_axis_length
        )
        horizontal_axis_height = HorizontalAxis.calculate_height(
                font=label_font)
        total_height = bbox.urc.y - bbox.llc.y
        vertical_axis_length = total_height - 2 * horizontal_axis_height
        vertical_axis = VerticalAxis(
            label_font=label_font,
            data_range=(min(data_ys), max(data_ys)),
            p0=bbox.llc + core.Point(0, horizontal_axis_height),
            length=vertical_axis_length
        )

        return horizontal_axis, vertical_axis


class Axis:

    _MAX_NUM_CHARS = len('-#.##e-99')
    _LABEL_FORMAT = '.2e'


class HorizontalAxis(Axis):

    _MIN_LABEL_SEPARATION = 10

    def __init__(
            self,
            *,
            label_font,
            data_range,
            p0,
            length,
    ):
        axis_excess = LabeledTick.calculate_width(
                font=label_font,
                max_num_chars=self._MAX_NUM_CHARS,
                position=Position.DOWN,
                ) / 2

        label_height = LabeledTick.calculate_height(
                font=label_font,
                position=Position.DOWN,
                )
        axis_y = p0.y + label_height
        left_excess_axis = core.Line(
                core.Point(p0.x, axis_y),
                core.Point(p0.x + axis_excess, axis_y),
        )
        right_excess_axis = core.Line(
                core.Point(p0.x + length - axis_excess, axis_y),
                core.Point(p0.x + length, axis_y),
        )
        main_axis = core.Line(
                left_excess_axis.end,
                right_excess_axis.start,
        )

        tags = self._create_tags(
            label_font=label_font,
            main_axis_range=(main_axis.start.x, main_axis.end.x),
            data_range=data_range,
            axis_y=axis_y,
        )

        self.elements = [
                main_axis, left_excess_axis, right_excess_axis
        ] + tags
        self.material_range = (main_axis.start.x, main_axis.end.x)

    def _create_tags(
            self,
            *,
            label_font,
            main_axis_range,
            data_range,
            axis_y,
            ):

        max_label_width = LabeledTick.calculate_width(
                font=label_font,
                max_num_chars=self._MAX_NUM_CHARS,
                position=Position.DOWN,
                )
        # Half of the 1st and last labels stick out
        # so they constitute 1 max_label_width.
        gap = label_font.max_char_width
        axis_x0, axis_x1 = main_axis_range
        axis_len = axis_x1 - axis_x0
        num_labels = int(axis_len / (gap + max_label_width))
        assert num_labels >= 2  # nosec
        tag_locations = np.linspace(axis_x0, axis_x1, num_labels)
        tag_location_percentages = (tag_locations - axis_x0) / axis_len
        data_min, data_max = data_range
        data_delta = data_max - data_min
        tag_values = [
                percentage * data_delta + data_min
                for percentage in tag_location_percentages
        ]
        tags = [
            LabeledTick(
                label=label_font.parse(format(value, self._LABEL_FORMAT)),
                anchor=core.Point(x, axis_y),
                position=Position.DOWN,
                max_num_chars=self._MAX_NUM_CHARS,
            )
            for x, value in zip(tag_locations, tag_values)
        ]

        return tags

    @classmethod
    def calculate_height(cls, *, font):
        return LabeledTick.calculate_height(
                font=font, position=Position.DOWN)


class VerticalAxis(Axis):

    def __init__(
            self,
            *,
            label_font,
            data_range,
            p0,
            length,
    ):
        axis_excess = LabeledTick.calculate_height(
                font=label_font,
                position=Position.LEFT,
                ) / 2

        label_width = LabeledTick.calculate_width(
                font=label_font,
                max_num_chars=self._MAX_NUM_CHARS,
                position=Position.LEFT,
                )
        axis_x = p0.x + label_width
        bottom_excess_axis = core.Line(
                core.Point(axis_x, p0.y),
                core.Point(axis_x, p0.y + axis_excess),
        )
        top_excess_axis = core.Line(
                core.Point(axis_x, p0.y + length - axis_excess),
                core.Point(axis_x, p0.y + length),
        )
        main_axis = core.Line(
                bottom_excess_axis.end,
                top_excess_axis.start,
        )

        tags = self._create_tags(
            label_font=label_font,
            main_axis_range=(main_axis.start.y, main_axis.end.y),
            data_range=data_range,
            axis_x=axis_x,
        )

        self.elements = [
                main_axis, bottom_excess_axis, top_excess_axis
        ] + tags
        self.material_range = (main_axis.start.y, main_axis.end.y)

    def _create_tags(
            self,
            *,
            label_font,
            main_axis_range,
            data_range,
            axis_x
            ):

        label_height = LabeledTick.calculate_height(
                font=label_font,
                position=Position.LEFT,
                )
        # Half of the 1st and last labels stick out
        # so they constitute 1 label_height.
        gap = label_font.height * 2
        axis_y0, axis_y1 = main_axis_range
        axis_len = axis_y1 - axis_y0
        num_labels = int(axis_len / (gap + label_height))
        assert num_labels >= 2  # nosec
        tag_locations = np.linspace(axis_y0, axis_y1, num_labels)
        tag_location_percentages = (tag_locations - axis_y0) / axis_len
        data_min, data_max = data_range
        data_delta = data_max - data_min
        tag_values = [
                percentage * data_delta + data_min
                for percentage in tag_location_percentages
        ]
        tags = [
            LabeledTick(
                label=label_font.parse(format(value, self._LABEL_FORMAT)),
                anchor=core.Point(axis_x, y),
                position=Position.LEFT,
                max_num_chars=self._MAX_NUM_CHARS,
            )
            for y, value in zip(tag_locations, tag_values)
        ]

        return tags

    @classmethod
    def calculate_width(cls, *, font):
        return LabeledTick.calculate_width(
                font=font,
                max_num_chars=cls._MAX_NUM_CHARS,
                position=Position.LEFT,
                )
