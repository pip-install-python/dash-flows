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


class ToolbarNode(Component):
    """A ToolbarNode component.
ToolbarNode - Glass morphism styled node with a configurable toolbar

Keyword arguments:

- data (dict; required):
    Node data configuration object.

    `data` is a dict with keys:

    - label (boolean | number | string | dict | list; optional):
        Primary content to display in the node.

    - sublabel (string; optional):
        Secondary text displayed below the main label.

    - toolbar (boolean | number | string | dict | list; optional):
        Custom toolbar content - DashIconify or other components.

    - toolbarVisible (boolean; optional):
        Whether the toolbar is visible (default: shows when selected).

    - toolbarPosition (a value equal to: 'top', 'bottom', 'left', 'right'; optional):
        Position of the toolbar relative to the node.

    - toolbarAlign (a value equal to: 'start', 'center', 'end'; optional):
        Alignment of the toolbar ('start', 'center', 'end').

    - toolbarOffset (number; optional):
        Offset distance of the toolbar from the node.

    - toolbarStyle (dict; optional):
        Custom CSS styles for the toolbar.

    - style (dict; optional):
        Custom CSS styles for the node container.

    - handleStyle (dict; optional):
        Custom CSS styles for connection handles.

    - targetPosition (string; optional):
        Position for the target (input) handle.

    - sourcePosition (string; optional):
        Position for the source (output) handle.

    - showTargetHandle (boolean; optional):
        Whether to show the target handle (default: True).

    - showSourceHandle (boolean; optional):
        Whether to show the source handle (default: True).

- isConnectable (boolean; optional):
    Whether connections can be made to/from this node.

- selected (boolean; optional):
    Whether the node is currently selected."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'ToolbarNode'
    Data = TypedDict(
        "Data",
            {
            "label": NotRequired[typing.Any],
            "sublabel": NotRequired[str],
            "toolbar": NotRequired[typing.Any],
            "toolbarVisible": NotRequired[bool],
            "toolbarPosition": NotRequired[Literal["top", "bottom", "left", "right"]],
            "toolbarAlign": NotRequired[Literal["start", "center", "end"]],
            "toolbarOffset": NotRequired[NumberType],
            "toolbarStyle": NotRequired[dict],
            "style": NotRequired[dict],
            "handleStyle": NotRequired[dict],
            "targetPosition": NotRequired[str],
            "sourcePosition": NotRequired[str],
            "showTargetHandle": NotRequired[bool],
            "showSourceHandle": NotRequired[bool]
        }
    )


    def __init__(
        self,
        data: typing.Optional["Data"] = None,
        selected: typing.Optional[bool] = None,
        isConnectable: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['data', 'isConnectable', 'selected']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['data', 'isConnectable', 'selected']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ToolbarNode, self).__init__(**args)

setattr(ToolbarNode, "__init__", _explicitize_args(ToolbarNode.__init__))
