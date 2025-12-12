# AUTO GENERATED FILE - DO NOT EDIT

#' @export
nodeSearch <- function(className=NULL, focusOnSelect=NULL, highlightDuration=NULL, highlightOnSelect=NULL, isOpen=NULL, onClose=NULL, placeholder=NULL, searchKeys=NULL, style=NULL, zoomLevel=NULL) {
    
    props <- list(className=className, focusOnSelect=focusOnSelect, highlightDuration=highlightDuration, highlightOnSelect=highlightOnSelect, isOpen=isOpen, onClose=onClose, placeholder=placeholder, searchKeys=searchKeys, style=style, zoomLevel=zoomLevel)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'NodeSearch',
        namespace = 'dash_flows',
        propNames = c('className', 'focusOnSelect', 'highlightDuration', 'highlightOnSelect', 'isOpen', 'onClose', 'placeholder', 'searchKeys', 'style', 'zoomLevel'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
