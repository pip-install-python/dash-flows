% Auto-generated: do not edit by hand
\name{groupNode}

\alias{groupNode}

\title{GroupNode component}

\description{
GroupNode - Glass morphism styled container node that can hold other nodes Child nodes should have parentId set to this node's ID  IMPORTANT: Group nodes should have zIndex set lower than child nodes in the node definition to ensure proper layering.
}

\usage{
groupNode(data=NULL, selected=NULL)
}

\arguments{
\item{data}{Lists containing elements 'label', 'icon', 'style', 'labelstyle', 'resizable', 'minwidth', 'minheight'.
those elements have the following types:
  - label (logical | numeric | character | named list | unnamed list; optional): label content for the group - displayed above the group container
  - icon (logical | numeric | character | named list | unnamed list; optional): icon element to display next to the label
  - style (named list; optional): custom css styles for the group container
  - labelstyle (named list; optional): custom css styles for the label element
  - resizable (logical; optional): whether the group can be resized (default: true)
  - minwidth (numeric; optional): minimum width constraint for resizing
  - minheight (numeric; optional): minimum height constraint for resizing. Node data object containing label, icon, and styling options}

\item{selected}{Logical. Whether the group is currently selected}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

