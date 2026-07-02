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


class GroupNode(Component):
    """A GroupNode component.
GroupNode - A simple labeled group container for child nodes

This follows the React Flow pattern for group nodes:
- The node's width/height is controlled via the style prop on the node definition
- Child nodes use parentId to reference this node
- Child nodes can use extent: 'parent' to stay within bounds
- Supports collapse/expand via data.collapsed (managed by DashFlows toggleCollapseNode prop)

Unlike standard nodes, group nodes are rendered as simple containers
that React Flow manages for parent-child relationships.

Keyword arguments:

- id (string; optional):
    Node ID.

- data (dict; optional):
    Node data object containing label, icon, and styling options.

    `data` is a dict with keys:

    - label (boolean | number | string | dict | list; optional):
        Label content for the group - displayed in top-left corner.

    - icon (boolean | number | string | dict | list; optional):
        Icon element to display next to the label.

    - labelStyle (dict; optional):
        Custom CSS styles for the label element.

    - resizable (boolean; optional):
        Whether the group can be resized (default: True).

    - minWidth (number; optional):
        Minimum width constraint for resizing.

    - minHeight (number; optional):
        Minimum height constraint for resizing.

    - maxWidth (number; optional):
        Maximum width constraint for resizing.

    - maxHeight (number; optional):
        Maximum height constraint for resizing.

    - keepAspectRatio (boolean; optional):
        Maintain aspect ratio when resizing.

    - collapsed (boolean; optional):
        Whether the group is collapsed (managed by DashFlows
        toggleCollapseNode).

    - collapsedWidth (number; optional):
        Width when collapsed (default: 150).

    - collapsedHeight (number; optional):
        Height when collapsed (default: 50).

- selected (boolean; optional):
    Whether the group is currently selected."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'GroupNode'
    Data = TypedDict(
        "Data",
            {
            "label": NotRequired[typing.Any],
            "icon": NotRequired[typing.Any],
            "labelStyle": NotRequired[dict],
            "resizable": NotRequired[bool],
            "minWidth": NotRequired[NumberType],
            "minHeight": NotRequired[NumberType],
            "maxWidth": NotRequired[NumberType],
            "maxHeight": NotRequired[NumberType],
            "keepAspectRatio": NotRequired[bool],
            "collapsed": NotRequired[bool],
            "collapsedWidth": NotRequired[NumberType],
            "collapsedHeight": NotRequired[NumberType]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        data: typing.Optional["Data"] = None,
        selected: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'data', 'selected']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'selected']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(GroupNode, self).__init__(**args)

setattr(GroupNode, "__init__", _explicitize_args(GroupNode.__init__))
