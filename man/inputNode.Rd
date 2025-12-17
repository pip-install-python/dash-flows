% Auto-generated: do not edit by hand
\name{inputNode}

\alias{inputNode}

\title{InputNode component}

\description{
InputNode - Glass morphism styled node with only a source handle (no incoming connections) Features a green accent bar at the top  Uses CSS classes from glass-theme.css for styling, supporting: - Light/dark mode via colorMode prop or Mantine color scheme - Theme presets (glass, solid, minimal) - Custom CSS variable overrides via theme prop - Custom icons via DashIconify or any Dash component
}

\usage{
inputNode(data=NULL, isConnectable=NULL, selected=NULL)
}

\arguments{
\item{data}{Lists containing elements 'label', 'title', 'sublabel', 'body', 'icon', 'iconcolor', 'showicon', 'layout', 'multiline', 'style', 'classname', 'handlestyle', 'sourceposition', 'status', 'loadingvariant'.
those elements have the following types:
  - label (logical | numeric | character | named list | unnamed list; optional): primary content to display in the node (string or dash component)
  - title (logical | numeric | character | named list | unnamed list; optional): alias for label - use for clarity when also using body text
  - sublabel (character; optional): secondary text displayed below the main label
  - body (logical | numeric | character | named list | unnamed list; optional): body text displayed below title/sublabel
  - icon (logical | numeric | character | named list | unnamed list; optional): custom icon - dashiconify component or any dash component
  - iconcolor (character; optional): background color for the icon container
  - showicon (logical; optional): show/hide the input icon (default: true)
  - layout (a value equal to: 'stacked', 'horizontal'; optional): layout mode: 'stacked' (vertical) or 'horizontal' (icon left, text right)
  - multiline (logical; optional): allow multiline text wrapping
  - style (named list; optional): custom css styles for the node container
  - classname (character; optional): additional css class name
  - handlestyle (named list; optional): custom css styles for connection handles
  - sourceposition (character; optional): position for the source (output) handle
  - status (a value equal to: 'initial', 'loading', 'success', 'error'; optional): node status: 'initial', 'loading', 'success', 'error'
  - loadingvariant (a value equal to: 'border', 'overlay'; optional): loading animation variant: 'border' or 'overlay'. Node data configuration object containing display and behavior settings}

\item{isConnectable}{Logical. Whether connections can be made from this node}

\item{selected}{Logical. Whether the node is currently selected}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

