% Auto-generated: do not edit by hand
\name{groupNode}

\alias{groupNode}

\title{GroupNode component}

\description{
GroupNode - A simple labeled group container for child nodes  This follows the React Flow pattern for group nodes: - The node's width/height is controlled via the style prop on the node definition - Child nodes use parentId to reference this node - Child nodes can use extent: 'parent' to stay within bounds - Supports collapse/expand via data.collapsed (managed by DashFlows toggleCollapseNode prop)  Unlike standard nodes, group nodes are rendered as simple containers that React Flow manages for parent-child relationships.
}

\usage{
groupNode(id=NULL, data=NULL, selected=NULL)
}

\arguments{
\item{id}{Character. Node ID}

\item{data}{Lists containing elements 'label', 'icon', 'labelstyle', 'resizable', 'minwidth', 'minheight', 'maxwidth', 'maxheight', 'keepaspectratio', 'collapsed', 'collapsedwidth', 'collapsedheight'.
those elements have the following types:
  - label (logical | numeric | character | named list | unnamed list; optional): label content for the group - displayed in top-left corner
  - icon (logical | numeric | character | named list | unnamed list; optional): icon element to display next to the label
  - labelstyle (named list; optional): custom css styles for the label element
  - resizable (logical; optional): whether the group can be resized (default: true)
  - minwidth (numeric; optional): minimum width constraint for resizing
  - minheight (numeric; optional): minimum height constraint for resizing
  - maxwidth (numeric; optional): maximum width constraint for resizing
  - maxheight (numeric; optional): maximum height constraint for resizing
  - keepaspectratio (logical; optional): maintain aspect ratio when resizing
  - collapsed (logical; optional): whether the group is collapsed (managed by dashflows togglecollapsenode)
  - collapsedwidth (numeric; optional): width when collapsed (default: 150)
  - collapsedheight (numeric; optional): height when collapsed (default: 50). Node data object containing label, icon, and styling options}

\item{selected}{Logical. Whether the group is currently selected}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

