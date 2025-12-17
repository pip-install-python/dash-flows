% Auto-generated: do not edit by hand
\name{groupNode}

\alias{groupNode}

\title{GroupNode component}

\description{
GroupNode - A simple labeled group container for child nodes  This follows the React Flow pattern for group nodes: - The node's width/height is controlled via the style prop on the node definition - Child nodes use parentId to reference this node - Child nodes can use extent: 'parent' to stay within bounds  Unlike standard nodes, group nodes are rendered as simple containers that React Flow manages for parent-child relationships.
}

\usage{
groupNode(data=NULL, selected=NULL)
}

\arguments{
\item{data}{Lists containing elements 'label', 'icon', 'labelstyle', 'resizable', 'minwidth', 'minheight'.
those elements have the following types:
  - label (logical | numeric | character | named list | unnamed list; optional): label content for the group - displayed in top-left corner
  - icon (logical | numeric | character | named list | unnamed list; optional): icon element to display next to the label
  - labelstyle (named list; optional): custom css styles for the label element
  - resizable (logical; optional): whether the group can be resized (default: true)
  - minwidth (numeric; optional): minimum width constraint for resizing
  - minheight (numeric; optional): minimum height constraint for resizing. Node data object containing label, icon, and styling options}

\item{selected}{Logical. Whether the group is currently selected}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

