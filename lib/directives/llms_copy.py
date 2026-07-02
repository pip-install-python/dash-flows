import dash_mantine_components as dmc
from dash.development.base_component import Component
from dash_iconify import DashIconify
from markdown2dash import BaseDirective


class LlmsCopy(BaseDirective):
    """
    Render the per-page LLM copy button at the top of a documentation page.

    Usage in markdown:
        .. llms_copy::Page Title

    Renders a single button that copies `<origin>/<page-path>/llms.txt` to
    the clipboard. Paste the result into ChatGPT, Claude, or any LLM and
    they'll fetch the page's prose docs directly.

    The `llms.toon` and `page.json` buttons were removed in v0.5.0:
    `dash-improve-my-llms` 2.0 dropped both endpoints (Dash 4.3 MCP covers
    structured layout introspection natively).
    """
    NAME = "llms_copy"

    def render(self, renderer, title: str, content: str, **options) -> Component:
        safe_title = title.lower().replace(" ", "-").replace("/", "-")
        button_id = f"llm-copy-button-{safe_title}"

        button = dmc.Tooltip(
            dmc.Button(
                dmc.Group(
                    [DashIconify(icon="mdi:file-document-outline", width=14), "Copy llms.txt URL"],
                    gap=6,
                    wrap="nowrap",
                ),
                id=button_id,
                variant="subtle",
                color="gray",
                size="compact-sm",
                className="llms-copy-button",
            ),
            label="Copy this page's /llms.txt URL — paste into ChatGPT, Claude, or any LLM",
            position="top",
            withArrow=True,
        )

        return dmc.Box(button, c="dimmed", my="sm")
