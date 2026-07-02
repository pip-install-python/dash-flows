# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.types import NumberType  # noqa: F401
except ImportError:
    # Backwards compatibility for dash<=4.1.0
    if typing.TYPE_CHECKING:
        raise
    NumberType = typing.Union[  # noqa: F401
        typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
    ]

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]


class AnimatedSvgEdge(Component):
    """An AnimatedSvgEdge component.
AnimatedSvgEdge - An edge that animates a custom SVG element along the path
Useful for showing data flow direction or active connections

Keyword arguments:

- id (string; required):
    Unique identifier for the edge.

- data (dict; optional):
    Configuration data for the animated SVG edge.

    `data` is a dict with keys:

    - duration (number; optional):
        Animation duration in seconds.

    - shape (a value equal to: 'circle', 'rect', 'arrow', 'pulse'; optional):
        Shape to animate: 'circle', 'rect', 'arrow', 'pulse'.

    - size (number; optional):
        Size of the animated shape.

    - color (string; optional):
        Color of the animated shape.

    - count (number; optional):
        Number of shapes to animate along the path.

    - reverse (boolean; optional):
        Reverse the animation direction.

- markerEnd (boolean | number | string | dict | list; optional):
    Marker configuration for the edge end.

- markerStart (boolean | number | string | dict | list; optional):
    Marker configuration for the edge start.

- selected (boolean; optional):
    Whether the edge is currently selected.

- sourcePosition (string; optional):
    Position of the source handle ('top', 'bottom', 'left', 'right').

- sourceX (number; required):
    X coordinate of the edge source.

- sourceY (number; required):
    Y coordinate of the edge source.

- targetPosition (string; optional):
    Position of the target handle ('top', 'bottom', 'left', 'right').

- targetX (number; required):
    X coordinate of the edge target.

- targetY (number; required):
    Y coordinate of the edge target."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'AnimatedSvgEdge'
    Data = TypedDict(
        "Data",
            {
            "duration": NotRequired[NumberType],
            "shape": NotRequired[Literal["circle", "rect", "arrow", "pulse"]],
            "size": NotRequired[NumberType],
            "color": NotRequired[str],
            "count": NotRequired[NumberType],
            "reverse": NotRequired[bool]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        sourceX: typing.Optional[NumberType] = None,
        sourceY: typing.Optional[NumberType] = None,
        targetX: typing.Optional[NumberType] = None,
        targetY: typing.Optional[NumberType] = None,
        sourcePosition: typing.Optional[str] = None,
        targetPosition: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        markerEnd: typing.Optional[typing.Any] = None,
        markerStart: typing.Optional[typing.Any] = None,
        selected: typing.Optional[bool] = None,
        data: typing.Optional["Data"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'data', 'markerEnd', 'markerStart', 'selected', 'sourcePosition', 'sourceX', 'sourceY', 'style', 'targetPosition', 'targetX', 'targetY']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'markerEnd', 'markerStart', 'selected', 'sourcePosition', 'sourceX', 'sourceY', 'style', 'targetPosition', 'targetX', 'targetY']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'sourceX', 'sourceY', 'targetX', 'targetY']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(AnimatedSvgEdge, self).__init__(**args)

setattr(AnimatedSvgEdge, "__init__", _explicitize_args(AnimatedSvgEdge.__init__))
