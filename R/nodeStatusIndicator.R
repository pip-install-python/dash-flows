# AUTO GENERATED FILE - DO NOT EDIT

#' @export
nodeStatusIndicator <- function(children=NULL, className=NULL, loadingVariant=NULL, status=NULL, style=NULL) {
    
    props <- list(children=children, className=className, loadingVariant=loadingVariant, status=status, style=style)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'NodeStatusIndicator',
        namespace = 'dash_flows',
        propNames = c('children', 'className', 'loadingVariant', 'status', 'style'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
