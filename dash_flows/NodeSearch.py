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


class NodeSearch(Component):
    """A NodeSearch component.
NodeSearch - A search panel for finding and focusing nodes
Supports searching by node id, label, or data properties

Keyword arguments:

- className (string; optional):
    Additional CSS class name.

- focusOnSelect (boolean; default True):
    Whether to focus on the selected node.

- highlightDuration (number; default 2000):
    Duration of highlight effect in ms.

- highlightOnSelect (boolean; default True):
    Whether to highlight the selected node.

- isOpen (boolean; default False):
    Whether the search panel is open.

- placeholder (string; default 'Search nodes...'):
    Placeholder text for the search input.

- searchKeys (list of strings; default ['id', 'label', 'type', 'title', 'name']):
    Keys to search in node data (default: ['id', 'label', 'type']).

- zoomLevel (number; default 1.5):
    Zoom level when focusing on a node."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'NodeSearch'


    def __init__(
        self,
        isOpen: typing.Optional[bool] = None,
        onClose: typing.Optional[typing.Any] = None,
        placeholder: typing.Optional[str] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        searchKeys: typing.Optional[typing.Sequence[str]] = None,
        focusOnSelect: typing.Optional[bool] = None,
        highlightOnSelect: typing.Optional[bool] = None,
        highlightDuration: typing.Optional[NumberType] = None,
        zoomLevel: typing.Optional[NumberType] = None,
        **kwargs
    ):
        self._prop_names = ['className', 'focusOnSelect', 'highlightDuration', 'highlightOnSelect', 'isOpen', 'placeholder', 'searchKeys', 'style', 'zoomLevel']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['className', 'focusOnSelect', 'highlightDuration', 'highlightOnSelect', 'isOpen', 'placeholder', 'searchKeys', 'style', 'zoomLevel']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(NodeSearch, self).__init__(**args)

setattr(NodeSearch, "__init__", _explicitize_args(NodeSearch.__init__))
