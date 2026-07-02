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


class NodeStatusIndicator(Component):
    """A NodeStatusIndicator component.
NodeStatusIndicator - A wrapper component that shows status indicators around nodes
Status can be: "initial", "loading", "success", "error"
Loading variants: "border" (spinning border) or "overlay" (full overlay with spinner)

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The node content to wrap.

- className (string; optional):
    Additional CSS class name.

- loadingVariant (a value equal to: 'border', 'overlay'; default 'border'):
    Loading animation variant - \"border\" shows spinning border,
    \"overlay\" shows full overlay.

- status (a value equal to: 'initial', 'loading', 'success', 'error'; default 'initial'):
    The current status of the node."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'NodeStatusIndicator'


    def __init__(
        self,
        children: typing.Optional[ComponentType] = None,
        status: typing.Optional[Literal["initial", "loading", "success", "error"]] = None,
        loadingVariant: typing.Optional[Literal["border", "overlay"]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'className', 'loadingVariant', 'status', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'className', 'loadingVariant', 'status', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(NodeStatusIndicator, self).__init__(children=children, **args)

setattr(NodeStatusIndicator, "__init__", _explicitize_args(NodeStatusIndicator.__init__))
