% Auto-generated: do not edit by hand
\name{animatedSvgEdge}

\alias{animatedSvgEdge}

\title{AnimatedSvgEdge component}

\description{
AnimatedSvgEdge - An edge that animates a custom SVG element along the path Useful for showing data flow direction or active connections
}

\usage{
animatedSvgEdge(id=NULL, data=NULL, markerEnd=NULL, markerStart=NULL,
selected=NULL, sourcePosition=NULL, sourceX=NULL,
sourceY=NULL, style=NULL, targetPosition=NULL, targetX=NULL,
targetY=NULL)
}

\arguments{
\item{id}{Character. Unique identifier for the edge}

\item{data}{Lists containing elements 'duration', 'shape', 'size', 'color', 'count', 'reverse'.
those elements have the following types:
  - duration (numeric; optional): animation duration in seconds
  - shape (a value equal to: 'circle', 'rect', 'arrow', 'pulse'; optional): shape to animate: 'circle', 'rect', 'arrow', 'pulse'
  - size (numeric; optional): size of the animated shape
  - color (character; optional): color of the animated shape
  - count (numeric; optional): number of shapes to animate along the path
  - reverse (logical; optional): reverse the animation direction. Configuration data for the animated SVG edge}

\item{markerEnd}{Logical | numeric | character | named list | unnamed list. Marker configuration for the edge end}

\item{markerStart}{Logical | numeric | character | named list | unnamed list. Marker configuration for the edge start}

\item{selected}{Logical. Whether the edge is currently selected}

\item{sourcePosition}{Character. Position of the source handle ('top', 'bottom', 'left', 'right')}

\item{sourceX}{Numeric. X coordinate of the edge source}

\item{sourceY}{Numeric. Y coordinate of the edge source}

\item{style}{Named list. Custom CSS styles for the edge path}

\item{targetPosition}{Character. Position of the target handle ('top', 'bottom', 'left', 'right')}

\item{targetX}{Numeric. X coordinate of the edge target}

\item{targetY}{Numeric. Y coordinate of the edge target}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

