"""A hook-based Dash package with NO metadata: props live in the docstring
only (modelviewer's shape) — the third source lib/api_reference reads."""


class DocWidget:
    """A DocWidget component.
    Renders a widget from a docstring.

    Keyword arguments:

    - id (string; optional):
        The ID used to identify this component in Dash callbacks.

    - value (number; required):
        The value shown.
        Continued on a second line.

    - size (string; default 'md'):
        Which size.

    - setProps (func; optional):
        internal
    """
