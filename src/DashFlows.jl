
module DashFlows
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "1.2.0"

include("jl/animatedcirclenode.jl")
include("jl/animatednodeedge.jl")
include("jl/dashflows.jl")
include("jl/devtools.jl")
include("jl/resizablenode.jl")
include("jl/animatedsvgedge.jl")
include("jl/buttonedge.jl")
include("jl/dataedge.jl")
include("jl/floatingedge.jl")
include("jl/simplebezieredge.jl")
include("jl/smoothstepedge.jl")
include("jl/stepedge.jl")
include("jl/straightedge.jl")
include("jl/buttonhandle.jl")
include("jl/defaultnode.jl")
include("jl/groupnode.jl")
include("jl/inputnode.jl")
include("jl/nodesearch.jl")
include("jl/nodestatusindicator.jl")
include("jl/nodetooltip.jl")
include("jl/outputnode.jl")
include("jl/toolbarnode.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "dash_flows",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "dash_flows.min.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "dash_flows.min.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
