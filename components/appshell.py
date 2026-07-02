import dash_mantine_components as dmc
from dash import Output, Input, clientside_callback, dcc, page_container, State

from components.header import create_header
from components.navbar import create_navbar, create_navbar_drawer
from lib.constants import PRIMARY_COLOR


def create_appshell(data):
    return dmc.MantineProvider(
        id="m2d-mantine-provider",
        theme={
            # Core Color System
            "primaryColor": PRIMARY_COLOR,
            "primaryShade": {"light": 6, "dark": 8},

            # Typography System
            "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "fontFamilyMonospace": "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Courier New', monospace",
            "headings": {
                "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                "fontWeight": 600,
                "sizes": {
                    "h1": {"fontSize": "2.125rem", "lineHeight": 1.3, "fontWeight": 700},
                    "h2": {"fontSize": "1.625rem", "lineHeight": 1.35, "fontWeight": 700},
                    "h3": {"fontSize": "1.375rem", "lineHeight": 1.4, "fontWeight": 600},
                    "h4": {"fontSize": "1.125rem", "lineHeight": 1.45, "fontWeight": 600},
                    "h5": {"fontSize": "1rem", "lineHeight": 1.5, "fontWeight": 600},
                    "h6": {"fontSize": "0.875rem", "lineHeight": 1.5, "fontWeight": 600},
                }
            },
            "fontSizes": {
                "xs": "0.75rem",    # 12px
                "sm": "0.875rem",   # 14px
                "md": "1rem",       # 16px - base body text
                "lg": "1.125rem",   # 18px
                "xl": "1.25rem",    # 20px
            },
            "lineHeights": {
                "xs": 1.4,
                "sm": 1.45,
                "md": 1.55,  # For body text
                "lg": 1.6,
                "xl": 1.65,
            },

            # Spacing System (based on 4px unit)
            "spacing": {
                "xs": "0.5rem",   # 8px
                "sm": "0.75rem",  # 12px
                "md": "1rem",     # 16px
                "lg": "1.5rem",   # 24px
                "xl": "2rem",     # 32px
            },

            # Border Radius System
            "radius": {
                "xs": "0.25rem",  # 4px
                "sm": "0.375rem", # 6px
                "md": "0.5rem",   # 8px
                "lg": "0.75rem",  # 12px
                "xl": "1rem",     # 16px
            },
            "defaultRadius": "md",

            # Shadow System
            "shadows": {
                "xs": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                "sm": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
                "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
            },

            # Color Contrast
            "black": "#1a1b1e",  # Softer black instead of pure #000000
            "white": "#ffffff",
            "autoContrast": True,
            "luminanceThreshold": 0.3,

            # Custom Colors
            "colors": {
                "myColor": [
                    "#F2FFB6",
                    "#DCF97E",
                    "#C3E35B",
                    "#AAC944",
                    "#98BC20",
                    "#86AC09",
                    "#78A000",
                    "#668B00",
                    "#547200",
                    "#455D00",
                ]
            },

            # Global Component Styling
            "components": {
                "Button": {
                    "defaultProps": {
                        "fw": 500,
                        "radius": "md",
                    }
                },
                "Card": {
                    "defaultProps": {
                        "shadow": "sm",
                        "padding": "lg",
                        "radius": "md",
                        "withBorder": True,
                    }
                },
                "Paper": {
                    "defaultProps": {
                        "shadow": "xs",
                        "padding": "md",
                        "radius": "md",
                    }
                },
                "TextInput": {
                    "defaultProps": {
                        "radius": "md",
                    }
                },
                "Select": {
                    "defaultProps": {
                        "radius": "md",
                    }
                },
                "Title": {
                    "styles": {
                        "root": {
                            "marginBottom": "0.75rem"  # sm spacing
                        }
                    }
                },
                "Text": {
                    "defaultProps": {
                        "size": "md",
                    }
                },
                "Alert": {
                    "defaultProps": {
                        "radius": "md",
                    },
                    "styles": {"title": {"fontWeight": 600}}
                },
                "Badge": {
                    "defaultProps": {
                        "radius": "md",
                    },
                    "styles": {"root": {"fontWeight": 600}}
                },
                "Table": {
                    "defaultProps": {
                        "highlightOnHover": True,
                        "withTableBorder": True,
                        "verticalSpacing": "sm",
                        "horizontalSpacing": "md",
                        "striped": True,
                    }
                },
                "Anchor": {
                    "defaultProps": {
                        "underline": "hover",
                    }
                },
            },
        },
        children=[
            dcc.Location(id="url", refresh="callback-nav"),
            dcc.Store(id="color-scheme-storage", storage_type="local"),
            # Persists the desktop-navbar collapse state across reloads.
            # null/false = visible (default), true = collapsed.
            dcc.Store(id="desktop-navbar-collapsed", storage_type="local"),
            dmc.NotificationContainer(),
            dmc.AppShell(
                [
                    create_header(data),
                    create_navbar(data),
                    create_navbar_drawer(data),
                    dmc.AppShellMain(
                        children=page_container,
                        style={"minHeight": "calc(100vh - 70px)"}  # Full height minus header
                    ),
                ],
                id="m2d-appshell",
                header={"height": 70},
                padding="xl",
                navbar={
                    "width": 280,
                    "breakpoint": "md",  # Collapse on medium screens and below
                    "collapsed": {"mobile": True},
                },
                aside={
                    "width": 280,
                    "breakpoint": "xl",
                    "collapsed": {"desktop": False, "mobile": True},
                },
                withBorder=True,
            ),
        ],
    )


# Initialize theme from localStorage or browser preference on page load
clientside_callback(
    """
    function(pathname) {
        // Check if theme is already stored in localStorage
        const storedTheme = localStorage.getItem('color-scheme-storage');
        if (storedTheme) {
            try {
                const parsed = JSON.parse(storedTheme);
                return parsed;
            } catch (e) {
                // If parsing fails, fall through to default logic
            }
        }

        // Check browser preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }

        // Default to light theme
        return 'light';
    }
    """,
    Output("color-scheme-storage", "data"),
    Input("url", "pathname"),
)

# Apply theme from storage to MantineProvider
clientside_callback(
    """
    function(colorScheme) {
        // Default to light if no theme is set
        return colorScheme || 'light';
    }
    """,
    Output("m2d-mantine-provider", "forceColorScheme"),
    Input("color-scheme-storage", "data")
)

# Toggle theme when button is clicked
clientside_callback(
    """
    function(n_clicks, theme) {
        // Toggle between light and dark
        const newTheme = theme === 'dark' ? 'light' : 'dark';
        return newTheme;
    }
    """,
    Output("color-scheme-storage", "data", allow_duplicate=True),
    Input("color-scheme-toggle", "n_clicks"),
    State("color-scheme-storage", "data"),
    prevent_initial_call=True,
)


# ---------------------------------------------------------------------------
# Desktop navbar collapse (the Burger in the header)
# ---------------------------------------------------------------------------
# dmc.Burger does NOT expose n_clicks — its public API is just `opened`,
# which flips internally on click and emits as an Input. So the data flow is:
#
#     User click → Burger.opened flips → callbacks below fire
#         ├→ AppShell navbar prop re-emitted with collapsed.desktop = !opened
#         └→ desktop-navbar-collapsed store updated (for cross-reload persistence)
#
# On page load, a separate callback rehydrates Burger.opened from the store.

# Burger opened → AppShell navbar config + persisted store (single source of truth)
clientside_callback(
    """
    function(opened) {
        const navbar = {
            width: 280,
            breakpoint: 'md',
            collapsed: {mobile: true, desktop: opened !== true}
        };
        // opened === true means navbar visible → store false. Default true so a
        // first-time visitor (store === null) gets the navbar open.
        const storeValue = opened === true ? false : true;
        return [navbar, storeValue];
    }
    """,
    [
        Output("m2d-appshell", "navbar"),
        Output("desktop-navbar-collapsed", "data"),
    ],
    Input("desktop-navbar-toggle", "opened"),
)

# On first render, rehydrate the Burger from the persisted store.
# Pathname is just a once-per-load trigger; the State is the value we actually use.
clientside_callback(
    """
    function(_pathname, collapsed) {
        // null/false/undefined = navbar visible (opened=true)
        // true = navbar collapsed (opened=false)
        return collapsed !== true;
    }
    """,
    Output("desktop-navbar-toggle", "opened"),
    Input("url", "pathname"),
    State("desktop-navbar-collapsed", "data"),
)