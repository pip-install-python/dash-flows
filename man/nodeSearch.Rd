% Auto-generated: do not edit by hand
\name{nodeSearch}

\alias{nodeSearch}

\title{NodeSearch component}

\description{
NodeSearch - A search panel for finding and focusing nodes Supports searching by node id, label, or data properties
}

\usage{
nodeSearch(className=NULL, focusOnSelect=NULL, highlightDuration=NULL,
highlightOnSelect=NULL, isOpen=NULL, onClose=NULL,
placeholder=NULL, searchKeys=NULL, style=NULL,
zoomLevel=NULL)
}

\arguments{
\item{className}{Character. Additional CSS class name}

\item{focusOnSelect}{Logical. Whether to focus on the selected node}

\item{highlightDuration}{Numeric. Duration of highlight effect in ms}

\item{highlightOnSelect}{Logical. Whether to highlight the selected node}

\item{isOpen}{Logical. Whether the search panel is open}

\item{onClose}{Callback when the panel should close}

\item{placeholder}{Character. Placeholder text for the search input}

\item{searchKeys}{List of characters. Keys to search in node data (default: ['id', 'label', 'type'])}

\item{style}{Named list. Custom inline styles}

\item{zoomLevel}{Numeric. Zoom level when focusing on a node}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

