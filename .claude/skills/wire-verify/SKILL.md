---
name: wire-verify
description: Verify this repo's production deployment on the wire — healthz identity/build/geo, both content lanes, and the fleet's known verification traps. Run after every deploy, before every report.
---

Verify what is actually serving, not what was pushed. Evidence means
pasted output; a claim without the artifact is not verified.

1. **Resolve identity from the repo, not from memory**: the host from
   `lib/constants.py` `BASE_URL`; the expected app key from the
   fork-point identity in run.py (`SATELLITE_APP_KEY` default); the
   expected build from `git rev-parse HEAD`. Read `DIVERGENCES.md` —
   it may change what healthz is allowed to contain.

2. **Healthz**: `curl -s <BASE_URL>/healthz`
   - `app` equals this repo's key (an answer of `boilerplate` on a
     fork means identity fell back to the template's — a defect).
   - `build` equals HEAD. Mismatch = the deploy hasn't landed or CD
     verified a different artifact. Missing entirely = the platform
     variable is absent (check the boot log) — do not shrug it off.
   - `geo` block present on dash-improve-my-llms ≥ 2.7 (counts and
     flags only). ABSENT on ≥2.7 means the Docker dependency-layer
     cache trap fired: the floor moved in text but not in the image
     — unless DIVERGENCES.md records a deliberately minimal payload.
   - `geo.resolved` naming a country via cf-ipcountry proves the
     edge's country header reaches the app.

3. **Machine lane** — name the crawler, do not rely on curl's
   default UA (1.6.30): which document you get is the package's UA
   classification, and an unnamed agent can land in either lane
   (the template serves `curl/8.x` the crawler document; muicharts
   saw the browser one). Probe explicitly, and confirm from the
   body which lane answered:

       curl -s -A "Mozilla/5.0 (compatible; Googlebot/2.1; \
       +http://www.google.com/bot.html)" <BASE_URL>/

   The crawler document is small (tens of KB, not hundreds) and
   carries real prose, exactly one `<h1>` (strip HTML comments
   before counting) and no "Loading..." stub. Spot-check one
   content page's `/<page>/llms.txt`: markdown, not an HTML shell.
   If this host blocks AI vendors, its DIVERGENCES.md posture block
   says which paths 403 — check those with a vendor UA too, and
   treat a mismatch as either the posture drifting or the block
   drifting, never as noise.

4. **Browser lane**: with a browser User-Agent, the app shell must
   carry the visible prerender div (no `hidden` attribute) and the
   marked synchronous hide script. The two lanes are different
   documents — a fix proven on one is unproven on the other.

5. **Traps** (fleet-learned):
   - GET, not HEAD — HEAD omits the Link discovery headers.
   - CI-run watchers keyed on a commit sha can match Dependabot's
     runs on the same sha; key on the workflow path (`cd.yml`).
   - Cloudflare overwrites a spoofed `CF-IPCountry` at the edge —
     you cannot test geo denial by spoofing against production.
   - A 200 from a single UA proves nothing about bot classes: curl
     is CLI-exempt from vendor blocking; check a crawler UA against
     `/healthz` if this host blocks any vendor.

6. **Report** observed vs expected for each check, pasting the
   actual JSON/status lines. If the sandbox cannot reach the host,
   state exactly that and hand the commands to the owner — an
   unverified claim marked unverified is honest; unmarked it is not.
