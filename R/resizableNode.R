# AUTO GENERATED FILE - DO NOT EDIT

#' @export
resizableNode <- function(data=NULL, height=NULL, selected=NULL, width=NULL) {
    
    props <- list(data=data, height=height, selected=selected, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'ResizableNode',
        namespace = 'dash_flows',
        propNames = c('data', 'height', 'selected', 'width'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
