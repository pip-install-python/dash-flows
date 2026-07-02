# Task: Add a New Example

## Purpose
Create a new example app demonstrating a dash-flows feature.

## Parameters
- `NUMBER`: Two-digit example number (next sequential after existing)
- `NAME`: Snake_case name (e.g., `undo_redo`)
- `TITLE`: Human-readable title (e.g., `Undo and Redo`)

## Steps

1. **Determine the next example number**
   - Check `examples/` directory for the highest existing number
   - Use the next sequential number

2. **Create the example file**
   - Save as `examples/{NUMBER}_{NAME}.py`
   - Follow this template:

   ```python
   """
   Example {NUMBER}: {TITLE}
   Description of what this example demonstrates.
   """
   import dash
   from dash import html, dcc, callback, Input, Output, State
   import dash_flows

   app = dash.Dash(__name__)

   nodes = [
       {
           "id": "node-1",
           "type": "default",
           "data": {"label": "Node 1"},
           "position": {"x": 100, "y": 100},
       },
   ]

   edges = [
       {"id": "e1-2", "source": "node-1", "target": "node-2"},
   ]

   app.layout = html.Div([
       html.H1("{TITLE}"),
       html.P("Description of the example."),
       dash_flows.DashFlows(
           id="flow",
           nodes=nodes,
           edges=edges,
           style={"height": "600px", "border": "1px solid #ddd"},
           fitView=True,
           showControls=True,
           showMiniMap=True,
       ),
   ])

   if __name__ == "__main__":
       app.run(debug=True, port=80{NUMBER})
   ```

3. **Add callbacks if needed**
   - Use `prevent_initial_call=True` for user-triggered actions
   - Use `dash.no_update` to avoid unnecessary updates

4. **Test the example**
   ```bash
   python examples/{NUMBER}_{NAME}.py
   ```

5. **Update IMPLEMENTATION_PLAN.md** if the example covers a planned feature

## Verification
- [ ] Example runs without errors
- [ ] Flow renders with correct nodes and edges
- [ ] Callbacks work as expected
- [ ] Port number does not conflict with other examples