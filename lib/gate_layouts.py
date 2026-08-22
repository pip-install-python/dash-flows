"""The interactive gate — what a browser sees instead of a page it may not read.

Ported from pip-docs+ (`lib/page_visibility.py`, the gate-layout half) with the
boilerplate's fail postures: the verdict comes from
:func:`lib.access.resolve_page_access`, which falls OPEN for ``auth`` docs when
Clerk is unconfigured and CLOSED for ``admin`` surfaces — do not "fix" either
direction, both are deliberate (see that function's docstring).

The gate is a card at HTTP 200, not a redirect and not a 404: the URL stays
shareable, the machine twin at ``/<page>/llms.txt`` keeps its own verdict, and
the card is the account-creation funnel. When ``lib/auth_demos.py`` registers a
teaser for the page, a live interactive example renders at the top of the card
so the visitor sees exactly what an account unlocks.

Buttons carry the static ids ``#auth-gate-signup`` / ``#auth-gate-signin``,
handled by ``assets/auth_gate.js`` (satellite mode navigates to the primary
with a returnTo; local dev opens the Clerk modal). Those selectors are
deliberately disjoint from ``#clerk-login-button``, which the package's own
handler and ``lib/auth.py``'s capture-phase fixup already own.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def _sign_in_destination() -> str:
    from lib import access

    return access.sign_in_url() or "https://2plot.ai"


def _card(icon: str, color: str, title: str, body: str, extra=None):
    import dash_mantine_components as dmc
    from dash_iconify import DashIconify

    children = [
        DashIconify(icon=icon, width=56, color=f"var(--mantine-color-{color}-5)"),
        dmc.Title(title, order=3, ta="center"),
        dmc.Text(body, c="dimmed", ta="center", maw=440),
    ]
    if extra is not None:
        children.append(extra)
    return dmc.Center(
        dmc.Paper(
            dmc.Stack(children, align="center", gap="md", p="xl"),
            withBorder=True, radius="lg", shadow="md", p="xl", mt="10vh", maw=560,
        )
    )


def sign_in_layout(page_name: str, path: str | None = None):
    """Account-creation funnel card shown to signed-out visitors.

    With a registered teaser demo (lib.auth_demos) a live example renders at
    the top — no code, no docs — so the visitor sees what an account unlocks.
    """
    import dash_mantine_components as dmc
    from dash_iconify import DashIconify

    demo = None
    if path:
        try:
            from lib.auth_demos import build_demo

            demo = build_demo(path)
        except Exception:  # a broken demo table must never break the funnel
            demo = None

    if demo is not None:
        intro = (
            f"You're looking at a live preview of {page_name}. Create a free "
            "account to unlock the full documentation — every interactive "
            "example, the complete API reference, and the AI assistant."
        )
    else:
        intro = (
            f"“{page_name}” is available to registered users — a free account "
            "unlocks every component's live examples and full API docs."
        )

    message = dmc.Stack(
        [
            dmc.ThemeIcon(
                DashIconify(icon="tabler:lock", width=28),
                size=54, radius="xl", variant="light", color="teal",
            ),
            dmc.Title("Authentication required", order=3, ta="center"),
            dmc.Text(intro, c="dimmed", ta="center", maw=460),
            dmc.Group(
                [
                    dmc.Button(
                        "Create free account",
                        id="auth-gate-signup",
                        size="md",
                        variant="gradient",
                        gradient={"from": "teal", "to": "cyan"},
                        leftSection=DashIconify(icon="tabler:user-plus", width=18),
                    ),
                    dmc.Button(
                        "Sign in",
                        id="auth-gate-signin",
                        size="md",
                        variant="default",
                        leftSection=DashIconify(icon="tabler:login-2", width=18),
                    ),
                ],
                justify="center",
                gap="sm",
                mt="xs",
            ),
            dmc.Text(
                "Free forever — you'll be redirected straight back to this "
                f"page. Accounts live at {_sign_in_destination()}.",
                size="xs", c="dimmed", ta="center",
            ),
        ],
        align="center",
        gap="md",
        p="xl",
    )

    children = [message] if demo is None else [demo, dmc.Divider(), message]

    return dmc.Center(
        dmc.Paper(
            children,
            withBorder=True,
            radius="lg",
            shadow="xl",
            p=0,
            mt="4vh" if demo is not None else "10vh",
            mb="4vh",
            w="100%",
            maw=780 if demo is not None else 560,
            style={"overflow": "hidden"},
        ),
        px="md",
    )


def forbidden_layout(page_name: str):
    return _card(
        "tabler:shield-lock", "red", "Restricted documentation",
        f"“{page_name}” is limited to administrator accounts.",
    )


def hidden_layout():
    return _card(
        "tabler:eye-off", "gray", "404 — Page not available",
        "This page is not currently published.",
    )


def gated_layout(path: str, page_name: str, build_layout):
    """Wrap a page layout in the interactive gate.

    ``build_layout`` is the prebuilt component tree (or a zero-arg callable
    returning one). The returned function becomes the Dash page layout, so
    the verdict runs on every render — an env flip applies on the next
    navigation, no rebuild. ``**kwargs`` is required: Dash Pages forwards
    query params (including Clerk's ``?__clerk_handshake=``) into layout
    callables.
    """
    def layout(**kwargs):
        from lib import access

        verdict = access.resolve_page_access(path)
        if verdict == "hidden":
            return hidden_layout()
        if verdict == "sign_in":
            return sign_in_layout(page_name, path)
        if verdict == "forbidden":
            return forbidden_layout(page_name)
        return build_layout() if callable(build_layout) else build_layout

    return layout
