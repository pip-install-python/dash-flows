# AUTO GENERATED FILE - DO NOT EDIT

#' @export
groupNode <- function(data=NULL, selected=NULL) {
    
    props <- list(data=data, selected=selected)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'GroupNode',
        namespace = 'dash_flows',
        propNames = c('data', 'selected'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
