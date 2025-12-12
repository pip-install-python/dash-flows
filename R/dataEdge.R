# AUTO GENERATED FILE - DO NOT EDIT

#' @export
dataEdge <- function(id=NULL, data=NULL, markerEnd=NULL, markerStart=NULL, selected=NULL, source=NULL, sourcePosition=NULL, sourceX=NULL, sourceY=NULL, style=NULL, targetPosition=NULL, targetX=NULL, targetY=NULL) {
    
    props <- list(id=id, data=data, markerEnd=markerEnd, markerStart=markerStart, selected=selected, source=source, sourcePosition=sourcePosition, sourceX=sourceX, sourceY=sourceY, style=style, targetPosition=targetPosition, targetX=targetX, targetY=targetY)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DataEdge',
        namespace = 'dash_flows',
        propNames = c('id', 'data', 'markerEnd', 'markerStart', 'selected', 'source', 'sourcePosition', 'sourceX', 'sourceY', 'style', 'targetPosition', 'targetX', 'targetY'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
