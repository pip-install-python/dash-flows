# AUTO GENERATED FILE - DO NOT EDIT

#' @export
straightEdge <- function(id=NULL, data=NULL, label=NULL, labelStyle=NULL, markerEnd=NULL, markerStart=NULL, selected=NULL, sourceX=NULL, sourceY=NULL, style=NULL, targetX=NULL, targetY=NULL) {
    
    props <- list(id=id, data=data, label=label, labelStyle=labelStyle, markerEnd=markerEnd, markerStart=markerStart, selected=selected, sourceX=sourceX, sourceY=sourceY, style=style, targetX=targetX, targetY=targetY)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'StraightEdge',
        namespace = 'dash_flows',
        propNames = c('id', 'data', 'label', 'labelStyle', 'markerEnd', 'markerStart', 'selected', 'sourceX', 'sourceY', 'style', 'targetX', 'targetY'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
