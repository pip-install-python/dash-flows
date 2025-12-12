# AUTO GENERATED FILE - DO NOT EDIT

#' @export
smoothStepEdge <- function(id=NULL, data=NULL, label=NULL, labelStyle=NULL, markerEnd=NULL, markerStart=NULL, selected=NULL, sourcePosition=NULL, sourceX=NULL, sourceY=NULL, style=NULL, targetPosition=NULL, targetX=NULL, targetY=NULL) {
    
    props <- list(id=id, data=data, label=label, labelStyle=labelStyle, markerEnd=markerEnd, markerStart=markerStart, selected=selected, sourcePosition=sourcePosition, sourceX=sourceX, sourceY=sourceY, style=style, targetPosition=targetPosition, targetX=targetX, targetY=targetY)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'SmoothStepEdge',
        namespace = 'dash_flows',
        propNames = c('id', 'data', 'label', 'labelStyle', 'markerEnd', 'markerStart', 'selected', 'sourcePosition', 'sourceX', 'sourceY', 'style', 'targetPosition', 'targetX', 'targetY'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
