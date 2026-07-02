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


class StraightEdge(Component):
    """A StraightEdge component.
StraightEdge - Glass morphism styled straight line edge

Keyword arguments:

- id (string; required):
    Unique identifier for the edge.

- data (dict; optional):
    Additional data passed to the edge.

- label (boolean | number | string | dict | list; optional):
    Label text to display on the edge.

- labelStyle (dict; optional):
    Custom CSS styles for the label.

- markerEnd (boolean | number | string | dict | list; optional):
    Marker configuration for the edge end.

- markerStart (boolean | number | string | dict | list; optional):
    Marker configuration for the edge start.

- selected (boolean; optional):
    Whether the edge is currently selected.

- sourceX (number; required):
    X coordinate of the edge source.

- sourceY (number; required):
    Y coordinate of the edge source.

- targetX (number; required):
    X coordinate of the edge target.

- targetY (number; required):
    Y coordinate of the edge target."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'StraightEdge'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        sourceX: typing.Optional[NumberType] = None,
        sourceY: typing.Optional[NumberType] = None,
        targetX: typing.Optional[NumberType] = None,
        targetY: typing.Optional[NumberType] = None,
        label: typing.Optional[typing.Any] = None,
        labelStyle: typing.Optional[dict] = None,
        style: typing.Optional[typing.Any] = None,
        markerEnd: typing.Optional[typing.Any] = None,
        markerStart: typing.Optional[typing.Any] = None,
        data: typing.Optional[dict] = None,
        selected: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'data', 'label', 'labelStyle', 'markerEnd', 'markerStart', 'selected', 'sourceX', 'sourceY', 'style', 'targetX', 'targetY']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'label', 'labelStyle', 'markerEnd', 'markerStart', 'selected', 'sourceX', 'sourceY', 'style', 'targetX', 'targetY']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'sourceX', 'sourceY', 'targetX', 'targetY']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(StraightEdge, self).__init__(**args)

setattr(StraightEdge, "__init__", _explicitize_args(StraightEdge.__init__))
