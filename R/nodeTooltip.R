# AUTO GENERATED FILE - DO NOT EDIT

#' @export
nodeTooltip <- function(children=NULL, className=NULL, offset=NULL, position=NULL, showOnHover=NULL, style=NULL, tooltipClassName=NULL, tooltipContent=NULL, tooltipStyle=NULL) {
    
    props <- list(children=children, className=className, offset=offset, position=position, showOnHover=showOnHover, style=style, tooltipClassName=tooltipClassName, tooltipContent=tooltipContent, tooltipStyle=tooltipStyle)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'NodeTooltip',
        namespace = 'dash_flows',
        propNames = c('children', 'className', 'offset', 'position', 'showOnHover', 'style', 'tooltipClassName', 'tooltipContent', 'tooltipStyle'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
