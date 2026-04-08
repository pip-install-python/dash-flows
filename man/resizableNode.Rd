% Auto-generated: do not edit by hand
\name{resizableNode}

\alias{resizableNode}

\title{ResizableNode component}

\description{
ResizableNode - A node that can be resized by the user  This node supports embedding Dash components that will resize along with the node container. The node receives width/height from React Flow when resized.
}

\usage{
resizableNode(data=NULL, height=NULL, selected=NULL, width=NULL)
}

\arguments{
\item{data}{Lists containing elements 'label', 'handles', 'style', 'initialwidth', 'initialheight', 'minwidth', 'minheight', 'maxwidth', 'maxheight', 'keepaspectratio', 'padding', 'alignitems', 'justifycontent', 'flexdirection'.
those elements have the following types:
  - label (logical | numeric | character | named list | unnamed list; optional): content to render inside the node - can be string, react element, or dash component
  - handles (required): array of connection handles for this node. handles has the following type: list of lists containing elements 'id', 'type', 'position', 'style', 'isconnectable', 'isconnectablestart', 'isconnectableend', 'onconnect', 'isvalidconnection'.
those elements have the following types:
  - id (character; required): unique identifier for the handle
  - type (character; required): handle type: 'source' or 'target'
  - position (character; required): handle position: 'top', 'bottom', 'left', or 'right'
  - style (named list; optional): custom css styles for the handle
  - isconnectable (logical; optional): whether the handle can be connected
  - isconnectablestart (logical; optional): whether connections can start from this handle
  - isconnectableend (logical; optional): whether connections can end at this handle
  - onconnect (optional): callback when a connection is made
  - isvalidconnection (optional): validation function for connectionss
  - style (named list; optional): custom css styles for the node container
  - initialwidth (numeric; optional): initial width of the node before resize
  - initialheight (numeric; optional): initial height of the node before resize
  - minwidth (numeric; optional): minimum width constraint for resizing
  - minheight (numeric; optional): minimum height constraint for resizing
  - maxwidth (numeric; optional): maximum width constraint for resizing
  - maxheight (numeric; optional): maximum height constraint for resizing
  - keepaspectratio (logical; optional): maintain aspect ratio when resizing
  - padding (numeric; optional): padding inside the node content area
  - alignitems (character; optional): flexbox align-items value for content
  - justifycontent (character; optional): flexbox justify-content value for content
  - flexdirection (character; optional): flexbox flex-direction value for content. Node data object containing label, handles, and styling options}

\item{height}{Numeric. Current height of the node (set by React Flow during resize)}

\item{selected}{Logical. Whether the node is currently selected}

\item{width}{Numeric. Current width of the node (set by React Flow during resize)}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

