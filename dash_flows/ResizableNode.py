# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class ResizableNode(Component):
    """A ResizableNode component.
ResizableNode - A node that can be resized by the user

This node supports embedding Dash components that will resize
along with the node container. The node receives width/height
from React Flow when resized.

Keyword arguments:

- data (dict; required):
    Node data object containing label, handles, and styling options.

    `data` is a dict with keys:

    - label (boolean | number | string | dict | list; optional):
        Content to render inside the node - can be string, React
        element, or Dash component.

    - handles (list of dicts; required):
        Array of connection handles for this node.

        `handles` is a list of dicts with keys:

        - id (string; required):

            Unique identifier for the handle.

        - type (string; required):

            Handle type: 'source' or 'target'.

        - position (string; required):

            Handle position: 'top', 'bottom', 'left', or 'right'.

        - style (dict; optional):

            Custom CSS styles for the handle.

        - isConnectable (boolean; optional):

            Whether the handle can be connected.

        - isConnectableStart (boolean; optional):

            Whether connections can start from this handle.

        - isConnectableEnd (boolean; optional):

            Whether connections can end at this handle.

        - onConnect (optional):

            Callback when a connection is made.

        - isValidConnection (optional):

            Validation function for connections.

    - style (dict; optional):
        Custom CSS styles for the node container.

    - initialWidth (number; optional):
        Initial width of the node before resize.

    - initialHeight (number; optional):
        Initial height of the node before resize.

    - minWidth (number; optional):
        Minimum width constraint for resizing.

    - minHeight (number; optional):
        Minimum height constraint for resizing.

    - padding (number; optional):
        Padding inside the node content area.

    - alignItems (string; optional):
        Flexbox align-items value for content.

    - justifyContent (string; optional):
        Flexbox justify-content value for content.

    - flexDirection (string; optional):
        Flexbox flex-direction value for content.

- height (number; optional):
    Current height of the node (set by React Flow during resize).

- selected (boolean; default False):
    Whether the node is currently selected.

- width (number; optional):
    Current width of the node (set by React Flow during resize)."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'ResizableNode'
    DataHandles = TypedDict(
        "DataHandles",
            {
            "id": str,
            "type": str,
            "position": str,
            "style": NotRequired[dict],
            "isConnectable": NotRequired[bool],
            "isConnectableStart": NotRequired[bool],
            "isConnectableEnd": NotRequired[bool],
            "onConnect": NotRequired[typing.Any],
            "isValidConnection": NotRequired[typing.Any]
        }
    )

    Data = TypedDict(
        "Data",
            {
            "label": NotRequired[typing.Any],
            "handles": typing.Sequence["DataHandles"],
            "style": NotRequired[dict],
            "initialWidth": NotRequired[NumberType],
            "initialHeight": NotRequired[NumberType],
            "minWidth": NotRequired[NumberType],
            "minHeight": NotRequired[NumberType],
            "padding": NotRequired[NumberType],
            "alignItems": NotRequired[str],
            "justifyContent": NotRequired[str],
            "flexDirection": NotRequired[str]
        }
    )


    def __init__(
        self,
        data: typing.Optional["Data"] = None,
        selected: typing.Optional[bool] = None,
        width: typing.Optional[NumberType] = None,
        height: typing.Optional[NumberType] = None,
        **kwargs
    ):
        self._prop_names = ['data', 'height', 'selected', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['data', 'height', 'selected', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ResizableNode, self).__init__(**args)

setattr(ResizableNode, "__init__", _explicitize_args(ResizableNode.__init__))
