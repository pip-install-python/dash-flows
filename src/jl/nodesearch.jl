# AUTO GENERATED FILE - DO NOT EDIT

export nodesearch

"""
    nodesearch(;kwargs...)

A NodeSearch component.
NodeSearch - A search panel for finding and focusing nodes
Supports searching by node id, label, or data properties
Keyword arguments:
- `className` (String; optional): Additional CSS class name
- `focusOnSelect` (Bool; optional): Whether to focus on the selected node
- `highlightDuration` (Real; optional): Duration of highlight effect in ms
- `highlightOnSelect` (Bool; optional): Whether to highlight the selected node
- `isOpen` (Bool; optional): Whether the search panel is open
- `placeholder` (String; optional): Placeholder text for the search input
- `searchKeys` (Array of Strings; optional): Keys to search in node data (default: ['id', 'label', 'type'])
- `style` (Dict; optional): Custom inline styles
- `zoomLevel` (Real; optional): Zoom level when focusing on a node
"""
function nodesearch(; kwargs...)
        available_props = Symbol[:className, :focusOnSelect, :highlightDuration, :highlightOnSelect, :isOpen, :placeholder, :searchKeys, :style, :zoomLevel]
        wild_props = Symbol[]
        return Component("nodesearch", "NodeSearch", "dash_flows", available_props, wild_props; kwargs...)
end

