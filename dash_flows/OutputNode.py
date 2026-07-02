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


class OutputNode(Component):
    """An OutputNode component.
OutputNode - Glass morphism styled node with only a target handle (no outgoing connections)
Features a purple accent bar at the bottom

Uses CSS classes from glass-theme.css for styling, supporting:
- Light/dark mode via colorMode prop or Mantine color scheme
- Theme presets (glass, solid, minimal)
- Custom CSS variable overrides via theme prop
- Custom icons via DashIconify or any Dash component

Keyword arguments:

- data (dict; required):
    Node data configuration object containing display and behavior
    settings.

    `data` is a dict with keys:

    - label (boolean | number | string | dict | list; optional):
        Primary content to display in the node (string or Dash
        component).

    - title (boolean | number | string | dict | list; optional):
        Alias for label - use for clarity when also using body text.

    - sublabel (string; optional):
        Secondary text displayed below the main label.

    - body (boolean | number | string | dict | list; optional):
        Body text displayed below title/sublabel.

    - icon (boolean | number | string | dict | list; optional):
        Custom icon - DashIconify component or any Dash component.

    - iconColor (string; optional):
        Background color for the icon container.

    - showIcon (boolean; optional):
        Show/hide the output icon (default: True).

    - layout (a value equal to: 'stacked', 'horizontal'; optional):
        Layout mode: 'stacked' (vertical) or 'horizontal' (icon left,
        text right).

    - multiline (boolean; optional):
        Allow multiline text wrapping.

    - style (dict; optional):
        Custom CSS styles for the node container.

    - className (string; optional):
        Additional CSS class name.

    - handleStyle (dict; optional):
        Custom CSS styles for connection handles.

    - targetPosition (string; optional):
        Position for the target (input) handle.

    - status (a value equal to: 'initial', 'loading', 'success', 'error'; optional):
        Node status: 'initial', 'loading', 'success', 'error'.

    - loadingVariant (a value equal to: 'border', 'overlay'; optional):
        Loading animation variant: 'border' or 'overlay'.

    - smartHandles (boolean; optional):
        Enable smart handles mode - renders target handles on all 4
        sides for optimal edge routing.

- isConnectable (boolean; optional):
    Whether connections can be made to this node.

- selected (boolean; optional):
    Whether the node is currently selected."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'OutputNode'
    Data = TypedDict(
        "Data",
            {
            "label": NotRequired[typing.Any],
            "title": NotRequired[typing.Any],
            "sublabel": NotRequired[str],
            "body": NotRequired[typing.Any],
            "icon": NotRequired[typing.Any],
            "iconColor": NotRequired[str],
            "showIcon": NotRequired[bool],
            "layout": NotRequired[Literal["stacked", "horizontal"]],
            "multiline": NotRequired[bool],
            "style": NotRequired[dict],
            "className": NotRequired[str],
            "handleStyle": NotRequired[dict],
            "targetPosition": NotRequired[str],
            "status": NotRequired[Literal["initial", "loading", "success", "error"]],
            "loadingVariant": NotRequired[Literal["border", "overlay"]],
            "smartHandles": NotRequired[bool]
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

        super(OutputNode, self).__init__(**args)

setattr(OutputNode, "__init__", _explicitize_args(OutputNode.__init__))
