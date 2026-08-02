from pathlib import Path

import frontmatter
import dash_mantine_components as dmc
from dash import dcc, register_page
from dash import html

from lib.constants import OG_IMAGE_URL, PAGE_TITLE_PREFIX, SITE_DESCRIPTION

# `description=` and `image_url=` are BOTH load-bearing: Dash emits the
# og:/twitter: description and image tags for every page, and emits them
# EMPTY when either argument is missing — an empty og:image unfurls worse
# than none, because scrapers treat it as the declared image and render a
# blank card. tests/test_social_card.py pins both.
register_page(
    __name__,
    "/",
    title=PAGE_TITLE_PREFIX + "Home",
    description=SITE_DESCRIPTION,
    image_url=OG_IMAGE_URL,
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
            className="home-markdown",
            style={
                "maxWidth": "none",  # Allow Container to control width
            }
        )
    ]
)
