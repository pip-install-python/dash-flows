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
\item{id}{Character. }

\item{data}{Lists containing elements 'duration', 'shape', 'size', 'color', 'count', 'reverse'.
those elements have the following types:
  - duration (numeric; optional): animation duration in seconds
  - shape (a value equal to: 'circle', 'rect', 'arrow', 'pulse'; optional): shape to animate: 'circle', 'rect', 'arrow', 'pulse'
  - size (numeric; optional): size of the animated shape
  - color (character; optional): color of the animated shape
  - count (numeric; optional): number of shapes to animate along the path
  - reverse (logical; optional): reverse the animation direction. }

\item{markerEnd}{Logical | numeric | character | named list | unnamed list. }

\item{markerStart}{Logical | numeric | character | named list | unnamed list. }

\item{selected}{Logical. }

\item{sourcePosition}{Character. }

\item{sourceX}{Numeric. }

\item{sourceY}{Numeric. }

\item{style}{Named list. }

\item{targetPosition}{Character. }

\item{targetX}{Numeric. }

\item{targetY}{Numeric. }
}

\value{named list of JSON elements corresponding to React.js properties and their values}

