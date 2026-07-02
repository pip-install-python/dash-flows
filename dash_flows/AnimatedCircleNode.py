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


class AnimatedCircleNode(Component):
    """An AnimatedCircleNode component.
AnimatedCircleNode - A circular node designed for use with animated edges.
Features a distinctive pink circular design that works well with AnimatedNodeEdge
to create animated dot effects along connections.

Keyword arguments:

- data (dict; required):
    Node data object containing the label content.

    `data` is a dict with keys:

    - label (boolean | number | string | dict | list; optional):
        Content to display inside the circular node - can be string or
        React element."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'AnimatedCircleNode'
    Data = TypedDict(
        "Data",
            {
            "label": NotRequired[typing.Any]
        }
    )


    def __init__(
        self,
        data: typing.Optional["Data"] = None,
        **kwargs
    ):
        self._prop_names = ['data']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['data']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(AnimatedCircleNode, self).__init__(**args)

setattr(AnimatedCircleNode, "__init__", _explicitize_args(AnimatedCircleNode.__init__))
