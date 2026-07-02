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


class DataEdge(Component):
    """A DataEdge component.
DataEdge - An edge that displays data from the source node
Useful for showing data flow between nodes

Keyword arguments:

- id (string; required):
    Unique identifier for the edge.

- data (dict; optional):
    Configuration data for the data edge.

    `data` is a dict with keys:

    - key (string; required):
        Key to read from source node's data.

    - prefix (string; optional):
        Prefix to display before the value.

    - suffix (string; optional):
        Suffix to display after the value.

    - labelStyle (dict; optional):
        Custom label styles.

- markerEnd (boolean | number | string | dict | list; optional):
    Marker configuration for the edge end.

- markerStart (boolean | number | string | dict | list; optional):
    Marker configuration for the edge start.

- selected (boolean; optional):
    Whether the edge is currently selected.

- source (string; required):
    ID of the source node to read data from.

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
    _type = 'DataEdge'
    Data = TypedDict(
        "Data",
            {
            "key": str,
            "prefix": NotRequired[str],
            "suffix": NotRequired[str],
            "labelStyle": NotRequired[dict]
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
        source: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        markerEnd: typing.Optional[typing.Any] = None,
        markerStart: typing.Optional[typing.Any] = None,
        selected: typing.Optional[bool] = None,
        data: typing.Optional["Data"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'data', 'markerEnd', 'markerStart', 'selected', 'source', 'sourcePosition', 'sourceX', 'sourceY', 'style', 'targetPosition', 'targetX', 'targetY']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'markerEnd', 'markerStart', 'selected', 'source', 'sourcePosition', 'sourceX', 'sourceY', 'style', 'targetPosition', 'targetX', 'targetY']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'source', 'sourceX', 'sourceY', 'targetX', 'targetY']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DataEdge, self).__init__(**args)

setattr(DataEdge, "__init__", _explicitize_args(DataEdge.__init__))
