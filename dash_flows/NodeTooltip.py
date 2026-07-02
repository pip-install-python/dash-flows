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


class NodeTooltip(Component):
    """A NodeTooltip component.
NodeTooltip - A wrapper that displays a tooltip when hovered
Built on top of React Flow's NodeToolbar component

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The node content.

- className (string; optional):
    CSS class for the container.

- offset (number; default 10):
    Offset from the node in pixels.

- position (a value equal to: 'top', 'bottom', 'left', 'right'; default 'top'):
    Position of the tooltip relative to the node.

- showOnHover (boolean; default True):
    Show tooltip only on hover (default: True).

- tooltipClassName (string; optional):
    CSS class for the tooltip.

- tooltipContent (a list of or a singular dash component, string or number; optional):
    Content to display in the tooltip.

- tooltipStyle (dict; optional):
    Inline styles for the tooltip."""
    _children_props: typing.List[str] = ['tooltipContent']
    _base_nodes = ['tooltipContent', 'children']
    _namespace = 'dash_flows'
    _type = 'NodeTooltip'


    def __init__(
        self,
        children: typing.Optional[ComponentType] = None,
        tooltipContent: typing.Optional[ComponentType] = None,
        position: typing.Optional[Literal["top", "bottom", "left", "right"]] = None,
        offset: typing.Optional[NumberType] = None,
        className: typing.Optional[str] = None,
        tooltipClassName: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        tooltipStyle: typing.Optional[dict] = None,
        showOnHover: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'className', 'offset', 'position', 'showOnHover', 'style', 'tooltipClassName', 'tooltipContent', 'tooltipStyle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'className', 'offset', 'position', 'showOnHover', 'style', 'tooltipClassName', 'tooltipContent', 'tooltipStyle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(NodeTooltip, self).__init__(children=children, **args)

setattr(NodeTooltip, "__init__", _explicitize_args(NodeTooltip.__init__))
