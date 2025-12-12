% Auto-generated: do not edit by hand
\name{nodeStatusIndicator}

\alias{nodeStatusIndicator}

\title{NodeStatusIndicator component}

\description{
NodeStatusIndicator - A wrapper component that shows status indicators around nodes Status can be: "initial", "loading", "success", "error" Loading variants: "border" (spinning border) or "overlay" (full overlay with spinner)
}

\usage{
nodeStatusIndicator(children=NULL, className=NULL, loadingVariant=NULL,
status=NULL, style=NULL)
}

\arguments{
\item{children}{A list of or a singular dash component, string or number. The node content to wrap}

\item{className}{Character. Additional CSS class name}

\item{loadingVariant}{A value equal to: 'border', 'overlay'. Loading animation variant - "border" shows spinning border, "overlay" shows full overlay}

\item{status}{A value equal to: 'initial', 'loading', 'success', 'error'. The current status of the node}

\item{style}{Named list. Custom inline styles}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

