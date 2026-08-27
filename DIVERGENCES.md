# Divergences from the template

Every DELIBERATE difference between this repo and
dash-documentation-boilerplate, with its reason. This file is the
boundary between design and drift:

- Template syncs read this file FIRST and must not "restore" anything
  recorded here.
- A difference not recorded here is treated as drift and will be
  synced away.
- Record the divergence in the SAME commit that creates it — one
  line: what differs, why, and what the template would otherwise do.
- An empty list is a statement too: it means this repo intends to
  match the template exactly.

## This repo's divergences

### 1. Two repos share this tree: a component library and its satellite

`src/lib/` (React + @xyflow/react), `webpack.config.js`,
`package.json` and the generated `dash_flows/*.py` wrappers are the
**dash-flows component library**; everything the fleet recognises —
`run.py`, `lib/`, `pages/`, `docs/`, the batteries — is the satellite
that documents it. The template's Dockerfile says a docs site is a
Python app and that "if a fork genuinely builds JS components it adds
its own toolchain knowingly, not by inheritance". This is that fork,
and it added it knowingly.

The image is unaffected: the bundle (`dash_flows/dash_flows.min.js`)
is COMMITTED, so there is still no Node layer in the Dockerfile and
`.dockerignore` drops `node_modules/`, `src/` and `package-lock.json`.
A sync must not delete `package.json` as the vestigial dmc-inherited
copy the template removed in 1.6.9 — here it is the live toolchain.

Consequences a sync will also meet: `.github/workflows/ci.yml` carries
three jobs with no template analogue — `examples` (every example app
imports across a dash × python matrix), `package` (wheel build and
verify in a clean venv) and `lint-js` (the bundle parses).

### 2. The docs-site requirements file is `requirements-docs.txt`

Root `requirements.txt` holds only what `dash-generate-components`
needs to build the component wrappers (`dash[dev]`, dmc). Every spec
sentence about "requirements.txt" — the dimll floor, the Docker cache
bust, pip-audit's input — means `requirements-docs.txt` in this repo.
The Dockerfile copies that file, so **its bytes are the cache bust**.

### 3. `/healthz` is built in `run.py`, not `lib/health.py`

There is no `lib/health.py` and no `lib/asgi_routes.py` here. One
`_health_body(headers=None)` in run.py renders for all three backends
and always has, so neither defect template 1.6.10 fixed — a payload
snapshotted at registration, and a FastAPI route that built its own
body without `build` — ever existed in this fork. The payload shape is
this repo's own: `{ok, app, version, dash, reporting, python}` plus
`build` and `geo` when they apply.

Porting the template's file would create a SECOND source of truth for
a payload whose shape this fork does not share. What is ported is the
CONTRACT: per-request construction, the identity field, the geo
diagnostic, each backend handing its own framework's headers to the
resolver. `tests/test_healthz.py` carries those pins.

### 4. `app`'s no-env fallback is `"boilerplate"`, not `"unknown"`

`lib/satellite_reporter.py` is kept BYTE-IDENTICAL to the template's
(shasum is the fleet's acceptance check), so its `app_key()` fallback
is necessarily the template's key. Identity is claimed instead by
run.py's fork point — `os.environ.setdefault("SATELLITE_APP_KEY",
"flows")`, placed before any hub-facing import. Repairing the
fallback in the reporter would break the byte-identity the fleet
checks; a fallback of `"boilerplate"` reaching production means the
fork point stopped running, which is the failure worth detecting.
`tests/test_bulletin.py` and `tests/test_healthz.py` pin both halves.

### 5. `render.yaml` is `runtime: docker` — and declares no `PYTHON_VERSION`

The template's service is `runtime: python`, where Render honours a
`PYTHON_VERSION` env var and the Blueprint is a real Python
declaration. This service is `runtime: docker` with
`dockerfilePath: ./Dockerfile`: the image IS the runtime and that key
is inert. Declaring one anyway would put a decorative version string
in the Blueprint that a future session could mistake for the
platform's actual setting — the precise confusion spec item 5 exists
to end.

So the Dockerfile's `FROM python:X.Y-slim` is this fork's SINGLE
Python declaration. `tests/test_python_version.py` is adapted to
match: it holds the image tag, the CI matrix main, the CI/CD singleton
pins and the wire together, and it asserts that while the runtime is
docker, render.yaml declares no `PYTHON_VERSION` at all.

### 6. Two env names for the canonical origin

`APP_BASE_URL` (the network-wide name) wins; `DASH_FLOWS_BASE_URL` is
this repo's original name and is still honoured, so a deployment that
predates the network standard keeps working. `lib/constants.py`
documents the precedence at the point of use.

### 7. `.claude/` carries this fork's own kit beside the network kit

`agents/`, `support_files/` and `tasks/` are component-library
documentation — the React Flow patterns, the theming reference, the
add-a-node-type walkthrough — tracked since March 2026, five months
before the network kit existed. They are repository documentation, not
session scratch.

`.gitignore` therefore keeps the template's allow-list FORM and adds
exactly three re-includes for them. That is the deliberate choice: the
rule is not weakened, so everything else under `.claude/` stays
structurally uncommittable, which is the whole reason the allow-list
form was chosen over a blanket ignore.

`.claude/CLAUDE.md` is this repo's own guide, per the F1 pilots'
correction — the network role paragraph is adapted to a repo that
wears two hats, and the contract and traps sections are byte-verbatim.
`.claude/settings.json` additionally allow-lists the component
documentation this repo's library work reads (reactflow.dev,
eclipse.dev, dash.plotly.com, dash-mantine-components.com,
icon-sets.iconify.design) alongside the standard host + hub entries;
the template's own fork has no such need.

### 8. Some ported contracts live in differently-named test files

The template's `tests/test_pages.py` structure sweep and its
`tests/test_llms_routes.py` healthz pins live here as
`tests/test_prerender.py` and `tests/test_healthz.py`; the smoke_live
SSL source pin lives in `tests/test_smoke_live.py` rather than
`tests/test_auth_wiring.py` (the batch-1-accepted home). The contracts
are ported and the pins pass; only the filenames differ, and a sync
that adds the template's filenames alongside would duplicate them.

### 9. `scripts/smoke_live.py` carries two checks the template does not

The file is contract-class from template 1.6.29 (spec item 6) — the wake
loop, the retry ladder and the certifi-backed SSL context are ported
verbatim and a change to any of them belongs upstream first. Two checks
below them are this fork's own:

- **the hub-bulletin warning** (`fatal=False`): this host went live with
  `NETWORK_BULLETIN_URL` unset, which breaks nothing visibly — the banner
  just shows one generic tip and "No announcements." The deploy log is the
  only place that fact is ever surfaced. The template pins the empty-state
  text in a unit test instead and has never carried a live check.
- **the auth-probe skip line**: this site ships the gate DARK, so the
  `dashClerkAuth` probe skips on every run. Silence would read as "it
  passed"; the line says it ran and found no Clerk.

Both are additive, both are inside `main()`, and neither touches the ported
contract. `scripts/smoke_live.py` is therefore listed in the byte-owned
fence below — 1.6.28 shipped this file as block cargo for exactly one
round and landed it red on 7 of 12 forks, so the fence is cheap insurance
against a future block re-adding it.

### 10. The battery's SSL context is ahead of the template

`scripts/network_smoke.py` calls `urlopen` with an explicit certifi-backed
`SSL_CONTEXT`; the template's copy at 1.6.29 (5589318) still does not.
Without it, macOS Python — which has no OS trust-store integration — dies
in the handshake, `fetch_raw` raises after its retries, and the battery
reports a perfectly healthy host as DOWN. CI is Linux and never sees it.
`tests/test_network_smoke.py::test_battery_urlopens_pass_the_ssl_context`
is the source pin, the same shape as the smoke_live one in divergence 8.

Applied here on the ops seat's fleet instruction (2026-08-26) and reported
upstream. RETIRE this entry when the template adopts the same fix — at
that point the difference is gone, not deliberate.

*(Retirements: none yet. When one lands, mark it retired here rather
than deleting it — a record that overclaims teaches the next sync to
defend a line nobody is attacking.)*

## Byte-owned paths

Paths this fork owns byte-for-byte. The F3b fan-out never overwrites
a path listed here; everything else in the spec's `sync-verbatim`
block is the template's to update mechanically. Prose above explains
divergences; this block is the machine answer.

Repo-relative paths, one per line, `#` comments, no `..`; exactly one
block. Each line is a YAML LIST ITEM — `- path/to/file  # why` — which
this paragraph did not say until a path was first put in it here:
`tests/test_claude_kit.py` requires the `- ` and every fork's fence was
empty, so nothing had ever exercised the form. Reported upstream
2026-08-26; the sentence is the fix, not the pin. An EMPTY block means "the template owns every sync-verbatim
path here" — present so the absence is a statement. When the block
exists it is authoritative; a fork without it gets the conservative
mention heuristic (over-flags, never restores).

Re-audited 2026-08-26 against the three specs' blocks at template
1.6.29 (5589318 — the range file was renamed from `SYNC-1.6.22-1.6.27`
as it grew). The block still lists the same six paths, and all six are
template-owned here and byte-identical after the F3b fan-out landed
1.6.29's two changed kit files (`d0ae5af`): the three
`.claude/skills/*/SKILL.md`, `tests/test_claude_kit.py`,
`tests/test_auth_demos.py` and `.github/dependabot.yml`. Nothing in the
prose above makes a byte-level claim on any of them — divergence 8 names
test files, but none of them is a sync-verbatim path, and divergence 7's
re-includes are `.gitignore` content, which no block carries.

The one entry is `scripts/smoke_live.py`, and it is defensive rather than
current: 1.6.29 pulled that file back OUT of the block after one round,
so no block claims it today. But 1.6.28 did claim it, byte-copied it into
twelve forks and landed it red on seven — and this fork's copy carries two
additive checks of its own (divergence 9). If a later spec re-adds the
path, the fence is what keeps those two checks alive. The ported contract
half — wake loop, retry ladder, SSL context — is still tracked upstream
and updated by hand, which is what class `contract` means.

```yaml byte-owned
- scripts/smoke_live.py  # divergence 9; contract-class since 1.6.29
```
