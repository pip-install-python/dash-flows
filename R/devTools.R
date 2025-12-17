# AUTO GENERATED FILE - DO NOT EDIT

#' @export
devTools <- function(nodes=NULL) {
    
    props <- list(nodes=nodes)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DevTools',
        namespace = 'dash_flows',
        propNames = c('nodes'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
