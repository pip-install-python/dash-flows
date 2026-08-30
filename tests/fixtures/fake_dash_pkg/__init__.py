"""A two-component Dash package, as a fixture for lib/api_reference (1.6.38).

Real Dash packages ship react-docgen `metadata.json` next to `__init__`
and export one class per `displayName`; this mimics exactly that shape.
"""
__version__ = "9.9.9"


class FakeWidget:  # noqa: D101 - stands in for a generated component class
    pass


class FakeGauge:  # noqa: D101
    pass
