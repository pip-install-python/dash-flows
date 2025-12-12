# AUTO GENERATED FILE - DO NOT EDIT

#' @export
buttonHandle <- function(children=NULL, id=NULL, buttonClassName=NULL, buttonContent=NULL, buttonStyle=NULL, className=NULL, isConnectable=NULL, onClick=NULL, onConnect=NULL, position=NULL, showButton=NULL, style=NULL, type=NULL) {
    
    props <- list(children=children, id=id, buttonClassName=buttonClassName, buttonContent=buttonContent, buttonStyle=buttonStyle, className=className, isConnectable=isConnectable, onClick=onClick, onConnect=onConnect, position=position, showButton=showButton, style=style, type=type)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'ButtonHandle',
        namespace = 'dash_flows',
        propNames = c('children', 'id', 'buttonClassName', 'buttonContent', 'buttonStyle', 'className', 'isConnectable', 'onClick', 'onConnect', 'position', 'showButton', 'style', 'type'),
        package = 'dashFlows'
        )

    structure(component, class = c('dash_component', 'list'))
}
