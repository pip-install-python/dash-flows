% Auto-generated: do not edit by hand
\name{smoothStepEdge}

\alias{smoothStepEdge}

\title{SmoothStepEdge component}

\description{
SmoothStepEdge - Glass morphism styled stepped edge with rounded corners
}

\usage{
smoothStepEdge(id=NULL, data=NULL, label=NULL, labelStyle=NULL,
markerEnd=NULL, markerStart=NULL, selected=NULL,
sourcePosition=NULL, sourceX=NULL, sourceY=NULL, style=NULL,
targetPosition=NULL, targetX=NULL, targetY=NULL)
}

\arguments{
\item{id}{Character. Unique identifier for the edge}

\item{data}{Named list. Additional data passed to the edge (borderRadius can be set here)}

\item{label}{Logical | numeric | character | named list | unnamed list. Label text to display on the edge}

\item{labelStyle}{Named list. Custom CSS styles for the label}

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

