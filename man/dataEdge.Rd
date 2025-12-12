% Auto-generated: do not edit by hand
\name{dataEdge}

\alias{dataEdge}

\title{DataEdge component}

\description{
DataEdge - An edge that displays data from the source node Useful for showing data flow between nodes
}

\usage{
dataEdge(id=NULL, data=NULL, markerEnd=NULL, markerStart=NULL,
selected=NULL, source=NULL, sourcePosition=NULL,
sourceX=NULL, sourceY=NULL, style=NULL, targetPosition=NULL,
targetX=NULL, targetY=NULL)
}

\arguments{
\item{id}{Character. }

\item{data}{Lists containing elements 'key', 'prefix', 'suffix', 'labelstyle'.
those elements have the following types:
  - key (character; required): key to read from source node's data
  - prefix (character; optional): prefix to display before the value
  - suffix (character; optional): suffix to display after the value
  - labelstyle (named list; optional): custom label styles. }

\item{markerEnd}{Logical | numeric | character | named list | unnamed list. }

\item{markerStart}{Logical | numeric | character | named list | unnamed list. }

\item{selected}{Logical. }

\item{source}{Character. }

\item{sourcePosition}{Character. }

\item{sourceX}{Numeric. }

\item{sourceY}{Numeric. }

\item{style}{Named list. }

\item{targetPosition}{Character. }

\item{targetX}{Numeric. }

\item{targetY}{Numeric. }
}

\value{named list of JSON elements corresponding to React.js properties and their values}

