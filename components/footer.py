"""The footer — identical on every host (1.6.38).

© {this year} Pip Install Python LLC · GitHub PROFILE · Discord · YouTube.
The repository link is the top bar's icon, the single Changelog link is
the sidebar's (owner, 2026-08-30). Every icon carries an accessible name;
the year is computed; no Terms/Privacy links until those pages exist.
"""
from datetime import datetime

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from lib.constants import DISCORD_URL, GITHUB_PROFILE_URL, PUBLISHER, YOUTUBE_SUBSCRIBE_URL

FOOTER_HEIGHT = 56


def _icon_link(icon, href, label):
    return dmc.Anchor(
        dmc.ActionIcon(
            DashIconify(icon=icon, width=20),
            size="lg",
            variant="subtle",
            color="gray",
            **{"aria-label": label},
        ),
        href=href,
        target="_blank",
        **{"aria-label": label},
    )


def create_footer():
    return dmc.AppShellFooter(
        dmc.Container(
            dmc.Group(
                [
                    dmc.Text(f"© {datetime.now().year} {PUBLISHER}", size="sm", c="dimmed"),
                    dmc.Group(
                        [
                            _icon_link("radix-icons:github-logo", GITHUB_PROFILE_URL, "Pip Install Python on GitHub"),
                            _icon_link("ic:baseline-discord", DISCORD_URL, "Join the 2plot Discord"),
                            _icon_link("mdi:youtube", YOUTUBE_SUBSCRIBE_URL, "Subscribe on YouTube"),
                        ],
                        gap="sm",
                    ),
                ],
                justify="space-between",
                wrap="nowrap",
            ),
            fluid=True,
            px="md",
            h="100%",
            style={"display": "flex", "alignItems": "center"},
        ),
        h=FOOTER_HEIGHT,
        withBorder=True,
    )
