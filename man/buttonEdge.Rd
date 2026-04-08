% Auto-generated: do not edit by hand
\name{buttonEdge}

\alias{buttonEdge}

\title{ButtonEdge component}

\description{
ButtonEdge - Glass morphism styled edge with an interactive button and optional toolbar
}

\usage{
buttonEdge(id=NULL, data=NULL, label=NULL, labelStyle=NULL,
markerEnd=NULL, markerStart=NULL, selected=NULL,
sourcePosition=NULL, sourceX=NULL, sourceY=NULL, style=NULL,
targetPosition=NULL, targetX=NULL, targetY=NULL)
}

\arguments{
\item{id}{Character. Unique identifier for the edge}

\item{data}{Lists containing elements 'label', 'showbutton', 'buttonlabel', 'buttonstyle', 'buttontitle', 'onbuttonclick', 'showtoolbar', 'toolbarstyle'.
those elements have the following types:
  - label (logical | numeric | character | named list | unnamed list; optional): label text to display next to the button
  - showbutton (logical; optional): whether to show the button (default: true)
  - buttonlabel (character; optional): text/symbol to display on the button (default: '×')
  - buttonstyle (named list; optional): custom css styles for the button
  - buttontitle (character; optional): tooltip title for the button
  - onbuttonclick (optional): callback function when button is clicked
  - showtoolbar (logical; optional): show glass morphism toolbar when edge is selected
  - toolbarstyle (named list; optional): custom css styles for the toolbar container. Configuration data for the button edge}

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

