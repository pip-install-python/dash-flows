"""The shipped .claude/ development kit — the F1 fabric build (2026-08-24).

The kit is how every fork inherits the network's behavioral contract,
skills, and settings. These pins keep it shipped (the old blanket
`.claude/` ignore silently kept the project instructions local-only —
forks inherited NOTHING), keep it case-correct (macOS is
case-insensitive; the fleet's CI and Render are not), and keep each
fork's settings pointing at ITS OWN host rather than the template's.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent

KIT_FILES = (
    ".claude/CLAUDE.md",
    ".claude/settings.json",
    ".claude/skills/wire-verify/SKILL.md",
    ".claude/skills/sync-template/SKILL.md",
    ".claude/skills/report/SKILL.md",
    "DIVERGENCES.md",
)


def _ignored(path: str) -> bool:
    return (
        subprocess.run(
            ["git", "check-ignore", "-q", path], cwd=REPO
        ).returncode
        == 0
    )


def _in_repo(rel: str) -> bool:
    return ".." not in rel and not rel.startswith("/")


def _machine_fence(kind: str, text: str, where: str) -> None:
    """The shared pin for machine fences (```yaml sync-verbatim in specs,
    ```yaml byte-owned in DIVERGENCES.md): exactly one block, `- path`
    lines with `#` comments, every path repo-relative and real at HEAD.
    Empty is valid — an empty block is a statement, a missing one is an
    omission. Gate lines (the fan-out's adoption gates) are validated
    like paths — a typo'd gate gates nothing:

      `# requires: <path>` (1.6.23) — the block applies only where
        <path> exists. For paths no pre-existing file can occupy;
        where one can, the gate must name a contract instead
        (sync/README.md — flows' pre-existing CLAUDE.md, 1.6.28).
      `# requires-contract: <path> :: <clause>` (1.6.28) — the block
        applies only where <path> exists AND contains <clause>. The
        clause must be real in THIS repo's copy at HEAD too.
      `- <path>  # requires: <other>` (1.6.28) — per-file gate: the
        fan-out skips this one copy where <other> is absent, instead
        of gating the whole block (clerkhook: a lockdown fork has no
        lib/auth_demos.py, legitimately, and must still receive the
        rest)."""
    fences = re.findall(
        r"^```yaml " + kind + r"[ \t]*\n(.*?)^```[ \t]*$", text, re.M | re.S
    )
    assert len(fences) == 1, (
        f"{where}: expected exactly one ```yaml {kind} fence, "
        f"found {len(fences)}"
    )
    for raw in fences[0].splitlines():
        stripped = raw.strip()
        if re.match(r"#\s*requires-contract:", stripped):
            gate = re.match(
                r"#\s*requires-contract:\s*(.+?)\s*::\s*(.+)$", stripped
            )
            assert gate, (
                f"{where} {kind}: {raw!r} — `# requires-contract:` takes "
                "`<path> :: <clause>`; a malformed gate gates nothing"
            )
            req, clause = gate.group(1).strip(), gate.group(2).strip()
            assert _in_repo(req), (
                f"{where} {kind}: `# requires-contract:` path {req!r} "
                "escapes the repo"
            )
            assert (REPO / req).is_file(), (
                f"{where} {kind}: `# requires-contract:` names {req!r} "
                "which does not exist at HEAD — a typo'd gate gates nothing"
            )
            assert clause in (REPO / req).read_text(), (
                f"{where} {kind}: `# requires-contract:` clause {clause!r} "
                f"is not in this repo's own {req} — a typo'd clause gates "
                "nothing"
            )
            continue
        required = re.match(r"#\s*requires:\s*(.+)$", stripped)
        if required:
            req = required.group(1).strip()
            assert _in_repo(req), (
                f"{where} {kind}: `# requires:` path {req!r} escapes the repo"
            )
            assert (REPO / req).is_file(), (
                f"{where} {kind}: `# requires:` names {req!r} which does "
                "not exist at HEAD — a typo'd gate gates nothing"
            )
            continue
        entry, _, comment = raw.partition("#")
        entry = entry.strip()
        if not entry:
            continue
        assert entry.startswith("- "), (
            f"{where} {kind}: {raw!r} is not a `- path` line"
        )
        path = entry[2:].strip()
        assert _in_repo(path), (
            f"{where} {kind}: {path!r} escapes the repo"
        )
        assert (REPO / path).is_file(), (
            f"{where} {kind}: {path!r} does not exist at HEAD "
            "— the machine would act on nothing or the wrong thing"
        )
        # A per-file gate is the WHOLE trailing comment, `requires: <path>`
        # from its first character; prose comments that merely mention the
        # word stay prose.
        per_file = re.match(r"\s*requires:\s*(.+)$", comment)
        if per_file:
            gate_path = per_file.group(1).strip()
            assert _in_repo(gate_path), (
                f"{where} {kind}: per-file gate on {path!r} escapes the "
                f"repo: {gate_path!r}"
            )
            assert (REPO / gate_path).is_file(), (
                f"{where} {kind}: per-file gate on {path!r} names "
                f"{gate_path!r} which does not exist at HEAD — a typo'd "
                "gate gates nothing"
            )


def test_kit_files_exist_and_are_not_ignored():
    """The blanket `.claude/` ignore kept the contract local-only for the
    template's whole life — every fork inherited nothing. The allow-list
    must keep these shippable."""
    for rel in KIT_FILES:
        assert (REPO / rel).is_file(), f"kit file missing: {rel}"
        assert not _ignored(rel), (
            f"{rel} is gitignored — the kit cannot propagate to forks"
        )


def test_local_and_scratch_stay_local():
    """settings.local.json is the per-seat model override and must never
    ship; session working documents are local by convention network-wide
    (two public repos were caught tracking theirs)."""
    for rel in (
        ".claude/settings.local.json",
        ".claude/scratch-probe.png",
        "HANDOFF-probe.md",
        "KICKOFF-probe.md",
        "X402-SYNC-REPORT.md",
    ):
        assert _ignored(rel), f"{rel} would be committable — must stay local"


def test_claude_md_is_case_canonical_and_carries_the_contract():
    """macOS tolerates `claude.md`; the fleet's Linux CI does not. And the
    contract section is the point of shipping the file at all."""
    assert "CLAUDE.md" in os.listdir(REPO / ".claude"), (
        ".claude/CLAUDE.md must be exact-case for case-sensitive systems"
    )
    body = (REPO / ".claude" / "CLAUDE.md").read_text()
    for clause in (
        "behavioral contract",
        "Check the prompt against this tree",
        "Corrections are your job",
        "Verify your own deploy on the wire",
        "DIVERGENCES.md",
    ):
        assert clause in body, f"contract clause missing from CLAUDE.md: {clause!r}"


def test_skills_carry_frontmatter():
    for name in ("wire-verify", "sync-template", "report"):
        text = (REPO / ".claude" / "skills" / name / "SKILL.md").read_text()
        head = text.split("---", 2)
        assert len(head) >= 3, f"{name}: SKILL.md has no frontmatter block"
        front = head[1]
        assert re.search(r"^name:\s*\S", front, re.M), f"{name}: no name"
        assert re.search(r"^description:\s*\S", front, re.M), f"{name}: no description"


def test_settings_point_at_this_forks_own_host():
    """The anti-drift pin: settings ship with the TEMPLATE's host, and a
    fork that keeps them verbatim gets a sandbox that can wire-verify the
    template instead of itself. BASE_URL is the identity source — the
    settings must follow it."""
    from lib.constants import BASE_URL

    host = urlparse(BASE_URL).hostname
    settings = json.loads((REPO / ".claude" / "settings.json").read_text())

    domains = settings["sandbox"]["network"]["allowedDomains"]
    assert host in domains, (
        f"sandbox.network.allowedDomains lacks this repo's own host {host!r} "
        "— sessions here could not wire-verify their own production. "
        "Fork ritual: replace the template's host with yours."
    )
    assert "2plot.ai" in domains, "the hub must stay reachable (boards, presence)"

    allows = settings.get("permissions", {}).get("allow", [])
    assert f"WebFetch(domain:{host})" in allows, (
        f"permissions.allow lacks WebFetch(domain:{host})"
    )


def test_sync_specs_are_specifiable():
    """F2: every sync spec item must carry class/detect/acceptance — an
    item without detect and acceptance is not specifiable (write a
    kickoff instead and fix the item until it is; sync/README.md).

    Skips where no sync/ exists: forks CONSUME specs, only the template
    authors them — emojimart's F2 correction: this file is a byte-
    verbatim kit port, and without the guard it failed on arrival at
    every fork. The pin wakes up the day a fork starts authoring specs.

    F3b: every spec also carries exactly one ```yaml sync-verbatim
    fence — the machine block the fan-out workflow byte-copies from.
    Every listed path must exist at HEAD and stay inside the repo; a
    wrong entry becomes twelve wrong PRs.
    """
    import pytest

    sync_dir = REPO / "sync"
    if not sync_dir.is_dir():
        pytest.skip("no sync/ — this repo consumes specs, it does not author them")
    assert (sync_dir / "README.md").is_file(), "sync/README.md (the format) missing"
    specs = sorted(sync_dir.glob("SYNC-*.md"))
    assert specs, "no sync specs — releases ship one (F2)"
    for spec in specs:
        text = spec.read_text()
        blocks = re.split(r"^### ", text, flags=re.M)[1:]
        assert blocks, f"{spec.name}: no items"
        for block in blocks:
            title = block.splitlines()[0]
            for field in ("class:", "detect:", "acceptance:"):
                assert field in block, (
                    f"{spec.name} item {title!r} lacks {field}"
                )

        _machine_fence("sync-verbatim", text, spec.name)


def test_divergences_carry_the_byte_owned_block():
    """F3b A1's finding: the fan-out honours DIVERGENCES.md by never
    overwriting a byte-owned path, and a prose MENTION over-flags —
    muicharts' host-pin nuance names tests/test_claude_kit.py while its
    bytes are template-owned, a false positive recurring every release.
    The fence is the machine answer; when present it is authoritative,
    and empty means "the template owns every sync-verbatim path here".

    ABSENCE SKIPS, never fails (1.6.22, the ops seat's own correction):
    the machine tolerates a missing fence (the mention heuristic —
    over-flags, never restores), so the pin must too. Failing here
    would let one unported contract item keep every later mechanical
    PR red, revoking the fan-out's "verbatim class = green merge"
    promise indefinitely. CI guards what a fork HAS declared; the
    spec's contract item and its session round drive adoption.
    """
    import pytest

    div = REPO / "DIVERGENCES.md"
    if not div.is_file():
        pytest.skip("no DIVERGENCES.md — nothing for the fan-out to honour")
    text = div.read_text()
    if not re.search(r"^```yaml byte-owned[ \t]*$", text, re.M):
        pytest.skip(
            "DIVERGENCES.md has no byte-owned fence — port "
            "SYNC-1.6.17-1.6.21 item 1; until then the fan-out uses the "
            "mention heuristic"
        )
    _machine_fence("byte-owned", text, "DIVERGENCES.md")
