from pathlib import Path

import frontmatter
import dash_mantine_components as dmc
from dash import dcc, register_page
from dash import html

from lib.constants import PAGE_TITLE_PREFIX

register_page(
    __name__,
    "/",
    title=PAGE_TITLE_PREFIX + "Home",
)

directory = "docs"

# read the home page markdown
md_file = Path("pages") / "home.md"

post = frontmatter.loads(md_file.read_text())
metadata, content = post.metadata, post.content

# Module-level LLMS_DOC — dash-improve-my-llms 2.0 picks this up automatically
# and serves it verbatim at /llms.txt. No layout walking, no extraction.
LLMS_DOC = content

layout = dmc.Container(
    size="lg",
    py="xl",
    children=[
        dcc.Markdown(
            content,
            style={
                "maxWidth": "none",  # Allow Container to control width
            }
        )
    ]
)
