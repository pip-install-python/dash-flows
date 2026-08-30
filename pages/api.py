"""/api — one prop table per component, generated from the package (1.6.38).

Registered ONLY when lib.constants.API_PACKAGES names something: the
template documents no component package, so on the template this module
registers nothing and the sidebar shows no API section. A fork declares
``API_PACKAGES = ["dash_mui_scheduler"]`` and gets the page, the sidebar
entry and the /api/llms.txt document for free.
"""
from __future__ import annotations

import dash
import dash_mantine_components as dmc
from dash import html

from lib import api_reference
from lib.constants import API_PACKAGES, OG_IMAGE_URL, PAGE_TITLE_PREFIX, SITE_SHORT_NAME


def prop_table(component: dict):
    head = dmc.TableThead(dmc.TableTr([dmc.TableTh(h) for h in ("prop", "type", "default", "description")]))
    rows = [
        dmc.TableTr([
            dmc.TableTd(dmc.Code(p["name"] + (" *" if p["required"] else ""))),
            dmc.TableTd(dmc.Text(p["type"], size="xs", ff="monospace")),
            dmc.TableTd(dmc.Code(p["default"]) if p["default"] else ""),
            dmc.TableTd(dmc.Text(p["description"], size="sm")),
        ])
        for p in component["props"]
    ]
    return dmc.Table([head, dmc.TableTbody(rows)], striped=True, highlightOnHover=True,
                     withTableBorder=True, fz="sm", id=f"api-table-{component['name']}")


def component_block(component: dict):
    return dmc.Stack(
        [dmc.Title(component["name"], order=3, id=f"api-{component['name']}"),
         dmc.Text(component["description"], c="dimmed", size="sm") if component["description"] else None,
         html.Div(prop_table(component), style={"overflowX": "auto"})],
        gap="xs",
    )


def build_page(packages=None):
    packages = API_PACKAGES if packages is None else packages
    blocks = [dmc.Title("API reference", order=1),
              dmc.Text(f"Every component {SITE_SHORT_NAME} documents, with its props — "
                       "generated from the installed package's metadata.", c="dimmed")]
    for pkg in api_reference.load_packages(packages):
        blocks.append(dmc.Title(pkg["package"], order=2, mt="lg"))
        if pkg.get("error"):
            blocks.append(dmc.Alert(pkg["error"], title="package not installed", color="yellow"))
        for c in pkg["components"]:
            blocks.append(component_block(c))
    return dmc.Container(dmc.Stack(blocks, gap="md"), id="m2d-page-api", size="lg", py="xl")


def layout(**kwargs):
    return build_page()


if API_PACKAGES:
    LLMS_DOC = api_reference.as_markdown(API_PACKAGES)
    dash.register_page(
        __name__,
        path="/api",
        name="API",
        title=PAGE_TITLE_PREFIX + "API",
        description=f"Component props reference for {', '.join(API_PACKAGES)}.",
        image_url=OG_IMAGE_URL,
        icon="mdi:api",
    )
