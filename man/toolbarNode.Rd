% Auto-generated: do not edit by hand
\name{toolbarNode}

\alias{toolbarNode}

\title{ToolbarNode component}

\description{
ToolbarNode - Glass morphism styled node with a configurable toolbar
}

\usage{
toolbarNode(data=NULL, isConnectable=NULL, selected=NULL)
}

\arguments{
\item{data}{Lists containing elements 'label', 'sublabel', 'toolbar', 'toolbarvisible', 'toolbarposition', 'toolbaralign', 'toolbaroffset', 'toolbarstyle', 'style', 'handlestyle', 'targetposition', 'sourceposition', 'showtargethandle', 'showsourcehandle'.
those elements have the following types:
  - label (logical | numeric | character | named list | unnamed list; optional): primary content to display in the node
  - sublabel (character; optional): secondary text displayed below the main label
  - toolbar (logical | numeric | character | named list | unnamed list; optional): custom toolbar content - dashiconify or other components
  - toolbarvisible (logical; optional): whether the toolbar is visible (default: shows when selected)
  - toolbarposition (a value equal to: 'top', 'bottom', 'left', 'right'; optional): position of the toolbar relative to the node
  - toolbaralign (a value equal to: 'start', 'center', 'end'; optional): alignment of the toolbar ('start', 'center', 'end')
  - toolbaroffset (numeric; optional): offset distance of the toolbar from the node
  - toolbarstyle (named list; optional): custom css styles for the toolbar
  - style (named list; optional): custom css styles for the node container
  - handlestyle (named list; optional): custom css styles for connection handles
  - targetposition (character; optional): position for the target (input) handle
  - sourceposition (character; optional): position for the source (output) handle
  - showtargethandle (logical; optional): whether to show the target handle (default: true)
  - showsourcehandle (logical; optional): whether to show the source handle (default: true). Node data configuration object}

\item{isConnectable}{Logical. Whether connections can be made to/from this node}

\item{selected}{Logical. Whether the node is currently selected}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

