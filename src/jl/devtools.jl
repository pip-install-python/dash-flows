# AUTO GENERATED FILE - DO NOT EDIT

export devtools

"""
    devtools(;kwargs...)

A DevTools component.
DevTools component for displaying debug information about the flow
Keyword arguments:
- `nodes` (required): Array of nodes to display information about. nodes has the following type: Array of lists containing elements 'id', 'type', 'position'.
Those elements have the following types:
  - `id` (String; required)
  - `type` (String; optional)
  - `position` (optional): . position has the following type: lists containing elements 'x', 'y'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)s
"""
function devtools(; kwargs...)
        available_props = Symbol[:nodes]
        wild_props = Symbol[]
        return Component("devtools", "DevTools", "dash_flows", available_props, wild_props; kwargs...)
end

