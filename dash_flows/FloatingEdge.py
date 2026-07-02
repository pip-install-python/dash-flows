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


class FloatingEdge(Component):
    """A FloatingEdge component.
FloatingEdge - Edge that connects to the nearest point on each node's border
instead of fixed handle positions. Creates more natural-looking connections.

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

- source (string; required):
    Source node ID.

- sourceX (number; optional):
    X coordinate of the edge source.

- sourceY (number; optional):
    Y coordinate of the edge source.

- target (string; required):
    Target node ID.

- targetX (number; optional):
    X coordinate of the edge target.

- targetY (number; optional):
    Y coordinate of the edge target."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'FloatingEdge'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        source: typing.Optional[str] = None,
        target: typing.Optional[str] = None,
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
        self._prop_names = ['id', 'data', 'label', 'labelStyle', 'markerEnd', 'markerStart', 'selected', 'source', 'sourceX', 'sourceY', 'style', 'target', 'targetX', 'targetY']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'label', 'labelStyle', 'markerEnd', 'markerStart', 'selected', 'source', 'sourceX', 'sourceY', 'style', 'target', 'targetX', 'targetY']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'source', 'target']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(FloatingEdge, self).__init__(**args)

setattr(FloatingEdge, "__init__", _explicitize_args(FloatingEdge.__init__))
