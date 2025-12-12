# AUTO GENERATED FILE - DO NOT EDIT

#' @export
defaultNode <- function(data=NULL, isConnectable=NULL, selected=NULL) {
    
    props <- list(data=data, isConnectable=isConnectable, selected=selected)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DefaultNode',
        namespace = 'dash_flows',
        propNames = c('data', 'isConnectable', 'selected'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
