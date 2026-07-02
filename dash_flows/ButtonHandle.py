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


class ButtonHandle(Component):
    """A ButtonHandle component.
ButtonHandle - A handle that can also function as a button
Useful for triggering actions when clicking on a connection point

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Child content for the button.

- id (string; optional):
    Unique identifier for the handle.

- buttonClassName (string; optional):
    CSS class for the button.

- buttonContent (a list of or a singular dash component, string or number; optional):
    Content to display in the button.

- buttonStyle (dict; optional):
    Inline styles for the button.

- className (string; optional):
    CSS class for the handle.

- isConnectable (boolean; default True):
    Whether the handle can connect to other nodes.

- position (a value equal to: 'top', 'bottom', 'left', 'right'; default 'bottom'):
    Position of the handle on the node.

- showButton (boolean; default False):
    Whether to show the button (default: False).

- type (a value equal to: 'source', 'target'; required):
    Type of handle - source or target."""
    _children_props: typing.List[str] = ['buttonContent']
    _base_nodes = ['buttonContent', 'children']
    _namespace = 'dash_flows'
    _type = 'ButtonHandle'


    def __init__(
        self,
        children: typing.Optional[ComponentType] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        type: typing.Optional[Literal["source", "target"]] = None,
        position: typing.Optional[Literal["top", "bottom", "left", "right"]] = None,
        isConnectable: typing.Optional[bool] = None,
        onClick: typing.Optional[typing.Any] = None,
        onConnect: typing.Optional[typing.Any] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        showButton: typing.Optional[bool] = None,
        buttonContent: typing.Optional[ComponentType] = None,
        buttonClassName: typing.Optional[str] = None,
        buttonStyle: typing.Optional[dict] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'buttonClassName', 'buttonContent', 'buttonStyle', 'className', 'isConnectable', 'position', 'showButton', 'style', 'type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'buttonClassName', 'buttonContent', 'buttonStyle', 'className', 'isConnectable', 'position', 'showButton', 'style', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['type']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ButtonHandle, self).__init__(children=children, **args)

setattr(ButtonHandle, "__init__", _explicitize_args(ButtonHandle.__init__))
