% Auto-generated: do not edit by hand
\name{devTools}

\alias{devTools}

\title{DevTools component}

\description{
DevTools component for displaying debug information about the flow
}

\usage{
devTools(nodes=NULL)
}

\arguments{
\item{nodes}{List of lists containing elements 'id', 'type', 'position'.
those elements have the following types:
  - id (character; required)
  - type (character; optional)
  - position (optional): . position has the following type: lists containing elements 'x', 'y'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)s. Array of nodes to display information about}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

