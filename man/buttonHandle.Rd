% Auto-generated: do not edit by hand
\name{buttonHandle}

\alias{buttonHandle}

\title{ButtonHandle component}

\description{
ButtonHandle - A handle that can also function as a button Useful for triggering actions when clicking on a connection point
}

\usage{
buttonHandle(children=NULL, id=NULL, buttonClassName=NULL,
buttonContent=NULL, buttonStyle=NULL, className=NULL,
isConnectable=NULL, onClick=NULL, onConnect=NULL,
position=NULL, showButton=NULL, style=NULL, type=NULL)
}

\arguments{
\item{children}{A list of or a singular dash component, string or number. Child content for the button}

\item{id}{Character. Unique identifier for the handle}

\item{buttonClassName}{Character. CSS class for the button}

\item{buttonContent}{A list of or a singular dash component, string or number. Content to display in the button}

\item{buttonStyle}{Named list. Inline styles for the button}

\item{className}{Character. CSS class for the handle}

\item{isConnectable}{Logical. Whether the handle can connect to other nodes}

\item{onClick}{Click handler for the button}

\item{onConnect}{Called when a connection is made}

\item{position}{A value equal to: 'top', 'bottom', 'left', 'right'. Position of the handle on the node}

\item{showButton}{Logical. Whether to show the button (default: false)}

\item{style}{Named list. Inline styles for the handle}

\item{type}{A value equal to: 'source', 'target'. Type of handle - source or target}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

