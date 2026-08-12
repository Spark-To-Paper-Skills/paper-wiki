"""idea_lint.py -- stdlib-only mechanical lint for paper-wiki idea, direction,
and goal cards.

Idea cards live at wiki/ideas/<slug>.md and follow the schema in
templates/research/WIKI.md.tmpl section "4b. idea 卡". Direction cards live
at wiki/directions/<slug>.md and follow section "4c. 方向卡". Goal cards live
at wiki/field/problems/<goal-id>.md and follow section "4e. goal 卡". This
script checks the double-column `## Claim` write-up discipline and the
surrounding structural rules mechanically for idea cards, the interrogative
direction-statement + four-section skeleton for direction cards, and the
six machine-checkable goal-card constraints (G1-G6) for goal cards, so all
three disciplines are enforced instead of being a paragraph of prose nobody
runs. Since 2026-08-12 (GSD 纪律移植) it additionally checks field/ files
stamped `maintainer: wiki-cartographer` (rule F1) and the idea-card
`important_problem` anchoring line (rule T1).

Usage:
    python scripts/idea_lint.py <card-path-or-dir> [<path> ...]

A path may be a single `.md` file or a directory (scanned recursively for
`*.md`). Files whose frontmatter is neither `type: idea`/`type: direction`
nor `kind: adopted-goal` nor `maintainer: wiki-cartographer` are skipped: a
file declaring an explicit but unsupported `type:` (e.g. a probe card) gets
a "skipped (unsupported type: X): path" line and is counted in the summary's
"(K skipped)" tail; files with no recognizable type/kind/maintainer at all
(e.g. a `problems.md` candidate list) stay silent, so pointing this at
`wiki/` is still safe.

Card type is dispatched by `card_type()`: idea cards run S1/S2/L1/L2/L3/L4/
L7/C2/C3/T1; direction cards run D1 only; goal cards run G1-G6 only; field
files run F1 only. The rule sets never cross-pollute -- a direction card is
never checked against S1/S2/L1/.../C3/T1 or G1-G6, an idea card is never
checked against D1 or G1-G6 or F1, a goal card is never checked against
S1/S2/.../C3/T1 or D1, and a field file only ever runs F1.

Card-type frontmatter keys are deliberately NOT interchangeable: idea/
direction/probe cards use `type:`, goal cards use `kind: adopted-goal` (not
`type: goal` -- goal cards are not a fifth note type, they are field-layer
material immune to the critic's adjudication gate; see WIKI.md.tmpl §4e).
`card_type()` checks both keys independently and never falls back from one
to the other -- a card missing both keys stays classified as "not a target
card, skip", matching the pre-existing behavior for field/ notes.

Rules implemented this milestone (idea cards -- S1/S2/L1/L2/L3/L4/L7/C2/C3):

    S1  structure           -- any of the 9 top-level sections missing;
                                `## Observation` empty or opening with
                                propose/design/提出; `## Claim` missing either
                                double-column subheading; Hypothesis column
                                missing a `Reframe:` sentence.
    S2  residual destination -- docs/llm-wiki.protocol.yaml
                                idea_lifecycle.residual_destination_rule made
                                mechanical: when frontmatter `status:` is
                                RETIRED or PARKED, `residual_destination`
                                must be non-empty (missing key, `null`, `""`,
                                or whitespace-only all count as missing) --
                                the one mechanically-checkable clause of the
                                "杀 idea 不杀资产" meta-rule. Violation is
                                anchored to the `residual_destination:` line
                                when that key exists at all (easier to fix),
                                falling back to the `status:` line only when
                                the key is missing outright. Any other
                                `status:` value is untouched by S2.
    L1  over-specification  -- the Claim double columns (Hypothesis(大胆版) /
                                当前可断言(assertable now)) contain concrete
                                instantiation numbers: parameter counts,
                                Chinese measure-unit counts ("635 例" etc.),
                                arXiv-style IDs, specific model names, or a
                                single named benchmark. The `#### delta`
                                subsection is excluded from this scan on
                                purpose -- citing a competitor's numbers there
                                is legitimate.
    L2  DoF annotation       -- every setting line under
                                `## Instantiation & DoF` must carry
                                [load-bearing] / [default] / [free].
    L3  load-bearing proof   -- every `[load-bearing]` line must be followed
                                (same line or the next) by a "(推导: ...)"
                                sentence, or be downgraded to [default].
    L4  pivot budget         -- `## Pivot rules` must list >= 2 `R<n>:` rules
                                (no experimental redundancy otherwise).
    L7  hedge budget         -- the Claim double columns together must not
                                exceed 2 hedge/qualifier hits (the canonical
                                template phrase "机制上可能源于" is exempted
                                before counting, so a compliant card is not
                                flagged by its own template).
    C2  evidence ceiling     -- the `### 当前可断言(assertable now)` column
                                must not use language stronger than the
                                card's evidence ceiling: the highest
                                lifecycle anchor ([w] < [p] < [e]) seen under
                                `## Observation`, defaulting to [w] when no
                                anchor is present at all. At ceiling [w], any
                                INDICATIVE_TERMS or ASSERTION_TERMS hit is a
                                violation; at ceiling [p], only
                                ASSERTION_TERMS hits are; a self-written [e]
                                anchor is itself a C2 violation (no experiment
                                ledger exists in v0 to certify it) and the
                                assertion scan proceeds at ceiling [p] (see C4
                                below). A second, independent
                                branch flags substantive assertable-column
                                prose when Observation carries zero anchors
                                at all ("无锚断言句"). `#### delta` is never
                                scanned (same exclusion as L1/L7).
    C3  indicative marker    -- a `[p: ...]` probe reference inside the
                                assertable column must share its line with
                                an INDICATIVE_TERMS word.
    T1  important_problem    -- 2026-08-12 用户批准移植 GSD 纪律(方案§三·5
        anchoring                谓词③,堵乙13「挂靠引不存在记录」)。当
                                frontmatter `important_problem:` 值非空(空/
                                null 不查)时:值必须含至少一个 `[[链接]]`,
                                且每个链接目标文件必须真实存在(与 dangling
                                检查同构)。wiki root 定位 = 沿
                                path.resolve().parents 找名为 'wiki' 的路径
                                组件,取其父目录为实例根;找不到 'wiki' 组件
                                则跳过存在性检查(生产实例的 idea 卡恒在
                                wiki/ideas/ 下,root 永远命中;examples/ 下
                                不在 wiki/ 内的既有 fixture 卡因此判定不变)。
                                注意:T1 不做「去重 >=2 个不同目标」检查——
                                红队原文(方案§四·5)把该补法钉在 field 条目
                                谓词④上并明说③是真死门无补法;在 T1 上加
                                去重会翻既有 fixture 基线,故不加。

Rules implemented this milestone (direction cards -- D1 only):

    D1  direction discipline -- the four-section skeleton
                                (`DIRECTION_SECTIONS`, verbatim from
                                WIKI.md.tmpl §4c) must all be present; the
                                `## 方向陈述` section's first non-blank line
                                must end in `？`/`?`. A declarative line that
                                co-occurs the idea-card Hypothesis template's
                                core verb phrase ("存在"/"表现出" together
                                with "机制上可能源于") gets an extra "疑似
                                idea 卡 Hypothesis 句伪装成方向卡" hint
                                appended to the same violation.

Rules implemented this milestone (goal cards -- G1/G2/G3/G4/G5/G6):

    NOTE: this G1-G6 set is a reconstructed candidate list, honestly flagged
    [ASSUMED] -- see the "Deferred" section below for the provenance caveat.

    G1  problem-statement       -- `## 问题陈述` (`GOAL_SECTIONS`, verbatim
        method-name ban            from WIKI.md.tmpl §4e) must not name a
                                    specific method: hits against
                                    `GOAL_METHOD_TERMS` / the idea-card
                                    `MODEL_NAME` list, or a "用 X 解决" /
                                    "通过 X 解决" solve-sentence pattern, are
                                    violations. A missing `## 问题陈述`
                                    section is itself a violation.
    G2  Success-criteria facet  -- every `## Success criteria` entry must
        coverage                    carry a `[facet: main|heldout|
                                    mechanism]` tag; main/heldout/mechanism
                                    each need >= 1 entry, any missing facet
                                    is a violation.
    G3  heldout no-real-name    -- entries tagged `[facet: heldout]` must
                                    not name a concrete dataset/benchmark
                                    (word list `GOAL_DATASET_TERMS`, plus the
                                    idea-card `BENCH_NAME` pattern) -- goal
                                    period bans naming the heldout object;
                                    that object is drawn by the method-blind
                                    party at experiment time (the role
                                    separation itself has no mechanical
                                    hook here -- tracked in
                                    ENFORCEMENT-MAP.md §3 by 05-07).
    G4  Admissibility anchor    -- every `## Admissibility` bullet must
                                    carry a `[[wikilink]]` or a `[w]`/`[p]`/
                                    `[e]` anchor tag -- the same anchor
                                    syntax direction cards' Wedges use
                                    (reuses the idea-card `OBS_ANCHOR_RE`
                                    tag shape via `ANCHOR_TAG_ANY_RE`). A
                                    missing `## Admissibility` section is
                                    itself a violation.
    G5  Non-goals empty/uncited -- `## Non-goals` must not be empty; any
                                    bullet claiming a partially-solved
                                    carve-out ("partially-solved"/"部分解决")
                                    must carry a `[[ledger 条目]]` wikilink.
    G6  Attack-surface count    -- `## Attack surface` must carry >= 2
                                    `[[wikilink]]` entries.

Rules implemented for field/ files (F1 only -- 2026-08-12 用户批准移植 GSD
纪律,方案§三·5 谓词④ + 红队#5 补法):

    F1  field-entry citations   -- files stamped `maintainer:
                                    wiki-cartographer` in frontmatter (field
                                    files carry no `type:` key; the silent
                                    skip is narrowed only for
                                    maintainer-stamped files). Every `## `
                                    entry must carry >= 3 `[[引用]]` links
                                    (堵乙15「field 条目 <3 篇出处无人查」--
                                    把 agents/wiki-cartographer.md 的
                                    '3-paper bar' prompt 级规则搬到输出级)
                                    AND the links must point to >= 2
                                    distinct targets after stripping
                                    `|alias`/`#fragment` (红队#5 补法,封
                                    「引同一篇三次凑数」). Goal cards are
                                    explicitly exempt: `kind: adopted-goal`
                                    dispatches to the G branch, matching the
                                    schema's "not subject to field's
                                    >=3-paper claim rule"; a `problems.md`
                                    one-line candidate list has no `## `
                                    entries and trips nothing.

NOTE on evidence-strength notation: vendor prose calls the three C2 tiers
A0/A1/A2, but `## Attributability preconditions` already uses `A1:`/`A2:`/
`A3:` as its own entry-numbering prefix (rule_l3_load_bearing depends on
that numbering). To avoid grep/visual collision, A0/A1/A2 notation is used
only in prose and internal identifiers (`evidence_ceiling`,
`INDICATIVE_TERMS`, `ASSERTION_TERMS`) -- the bare tier number is never
followed by a colon and printed as a card-text or lint-message prefix the
way the Attributability entries are.

Exit codes: 0 = no violations found, 1 = one or more violations found,
2 = usage/IO error (path not found, or no `.md` files to check).

Deferred (explicitly NOT implemented this milestone -- see
.planning/phases/03-idea-card-relayer/03-RESEARCH.md Design Extraction §6 and
the CONTEXT.md "宁窄勿宽" decision; tracked for ENFORCEMENT-MAP.md §2 in a
later plan):

    L5  Predictions completeness (>= 2 conditions, >= 1 strong)
    L6  Attributability preconditions non-empty
    hedge judgment-backing rule (every hedge term must trace to a standing
        verdict in wiki/novelty/ledger.md)
    pivot gradient budget (> 3 tiers per [default] dimension)
    C4  experiment-level assertion ceiling -- overclaim gated at an [e]
        (experiment-level) evidence ceiling. The [e] anchor only becomes
        legitimately producible once an orchestrator ledger exists to certify
        experiment-level results, and no such ledger is built this milestone
        (see 04-RESEARCH.md Design Extraction §3a). C4 stays deferred, but C2
        now rejects an [e] appearance outright: a self-written [e] anchor is
        flagged as a C2 violation and the assertion scan proceeds at ceiling
        [p]. Tracked for ENFORCEMENT-MAP.md §2.

G1-G6 provenance (honest [ASSUMED] flag -- see 05-RESEARCH.md Design
Extraction §6 and Assumptions Log A3): vendor's `goal-first-v1.md` says the
original G-L lint set had 10 rules, red-teamed down to "~6, merged into a
single lint script" -- but gives no literal G-L clause text. The complete
original list lives in `goal-first-full-report.json`'s
`design.blueprint_deltas` field, which is outside this phase's required
reading. The G1-G6 set above is this phase's reconstruction of the *simplest
candidate set* from the mechanical constraints stated verbatim in the
six-part goal-card prose (WIKI.md.tmpl §4e) -- it is NOT a literal recovery
of the original 10-item G-L numbering, and it is not claimed to be. If a
future plan obtains `goal-first-full-report.json` in full, it should replace
this table with the original literal G-L numbering rather than treat G1-G6
as canonical.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Canonical schema -- must match templates/research/WIKI.md.tmpl section 4b
# verbatim. Do not rewrite these names from memory; they come from the
# finalized idea-card schema.
# ---------------------------------------------------------------------------

TOP_SECTIONS = [
    "Observation",
    "Surprise & rule-out",
    "Claim",
    "Scope conditions",
    "Predictions",
    "Attributability preconditions",
    "Instantiation & DoF",
    "Pivot rules",
    "实验台账",
]

TOP_HEADER_RE = re.compile(r"^## (.+?)\s*$")
SUB_HEADER_RE = re.compile(r"^### (.+?)\s*$")
DELTA_HEADER_RE = re.compile(r"^#### delta\s*$")

# The double-column subheadings tolerate both ASCII () and full-width （）
# parentheses -- do not hardcode a single bracket style.
HYPOTHESIS_HEADER_RE = re.compile(r"^### Hypothesis[\(（].*[\)）]\s*$")
ASSERTABLE_HEADER_RE = re.compile(r"^### 当前可断言[\(（].*[\)）]\s*$")

IDEA_TYPE_RE = re.compile(r"(?m)^type:\s*idea\s*$")
DIRECTION_TYPE_RE = re.compile(r"(?m)^type:\s*direction\s*$")

# Goal cards use a *different* frontmatter key than idea/direction/probe
# cards -- `kind: adopted-goal`, never `type: goal` (see the module
# docstring's "Card-type frontmatter keys" note). This is intentionally its
# own regex, not folded into IDEA_TYPE_RE/DIRECTION_TYPE_RE's `type:` shape.
GOAL_KIND_RE = re.compile(r"(?m)^kind:\s*adopted-goal\s*$")

# Field files (wiki/field/assumptions.md 等三件) carry no `type:` key at all;
# their identifying frontmatter stamp is `maintainer: wiki-cartographer`
# (see agents/wiki-cartographer.md and WIKI.md.tmpl's 公共 frontmatter block).
# card_type() returns "field" on this stamp so rule F1 can run -- the
# pre-existing "no type key -> silently skipped" behavior is narrowed ONLY
# for maintainer-stamped files; every other typeless file stays silent.
FIELD_MAINTAINER_RE = re.compile(r"(?m)^maintainer:\s*wiki-cartographer\s*$")

# Raw `type:` value extractor -- used only by main()'s skip reporting to name
# the unsupported card type in the "skipped (unsupported type: X): path"
# line. Files with no `type:` key at all (e.g. field/ notes) stay silently
# skipped, preserving the pre-existing "pointing this at wiki/ is safe"
# behavior.
TYPE_LINE_RE = re.compile(r"(?m)^type:\s*(\S.*?)\s*$")

# Direction-card four-section skeleton -- must match
# templates/research/WIKI.md.tmpl section "4c. 方向卡" verbatim (the four
# `## ` headings in file order). Do NOT reuse TOP_SECTIONS -- direction cards
# are a separate note type with their own, much smaller, skeleton.
DIRECTION_SECTIONS = ["方向陈述", "Wedges", "平凡解释候选清单", "探针计划"]

# Goal-card six-section skeleton -- must match
# templates/research/WIKI.md.tmpl section "4e. goal 卡" verbatim (the six
# `## ` headings in file order). Copied by hand from the fenced schema block,
# not retyped from memory. Do NOT reuse TOP_SECTIONS/DIRECTION_SECTIONS --
# goal cards are their own note kind with their own skeleton.
GOAL_SECTIONS = [
    "问题陈述",
    "Success criteria",
    "Admissibility",
    "Non-goals",
    "Attack surface",
    "状态与 closure",
]

# Named aliases into GOAL_SECTIONS -- G-rule functions read section content
# through these instead of re-typing the literal strings, so the schema
# string and the rule lookups can never silently drift apart. The sixth
# entry (状态与 closure) has no dedicated G-rule: state/closure validity is
# enforced via docs/llm-wiki.protocol.yaml's `goal_lifecycle:` block, not by
# this lint script (see 05-RESEARCH.md Design Extraction §6 table -- G1-G6
# map onto goal-card sections 1-5 only).
(
    GOAL_SEC_PROBLEM,
    GOAL_SEC_SUCCESS_CRITERIA,
    GOAL_SEC_ADMISSIBILITY,
    GOAL_SEC_NON_GOALS,
    GOAL_SEC_ATTACK_SURFACE,
    GOAL_SEC_STATUS_CLOSURE,
) = GOAL_SECTIONS


# ---------------------------------------------------------------------------
# Card parsing
# ---------------------------------------------------------------------------


def read_card(
    path: Path,
) -> tuple[str, list[tuple[int, str]], list[tuple[int, str]]]:
    """Read a card as UTF-8 and split it into (frontmatter text, frontmatter
    lines, body lines).

    Frontmatter lines and body lines are both returned as lists of (1-based
    line number, text) tuples over the whole file -- callers slice by
    section, not by re-reading. `fm_text` is kept alongside `fm_lines` for
    backward compatibility with call sites (`card_type()`, `is_idea_card()`,
    the `*_TYPE_RE`/`GOAL_KIND_RE` regexes) that only need the raw frontmatter
    text, not per-line numbers; `fm_lines` exists so rules that need to
    anchor a violation to a specific frontmatter line (e.g. S2) don't have to
    re-derive line numbers from `fm_text` by hand. Frontmatter is only
    detected, never parsed as YAML: the file must open with a `---` line and
    have a matching closing `---` line.
    """
    text = path.read_text(encoding="utf-8")
    raw_lines = text.splitlines()
    numbered = list(enumerate(raw_lines, start=1))

    fm_text = ""
    fm_lines: list[tuple[int, str]] = []
    body_start = 0
    if raw_lines and raw_lines[0].strip() == "---":
        for i in range(1, len(raw_lines)):
            if raw_lines[i].strip() == "---":
                fm_text = "\n".join(raw_lines[1:i])
                fm_lines = numbered[1:i]
                body_start = i + 1
                break

    return fm_text, fm_lines, numbered[body_start:]


def split_sections(lines: list[tuple[int, str]]) -> dict[str, list[tuple[int, str]]]:
    """Split body lines into top-level (`## `) sections.

    Keys are the section title verbatim (text after `## `, trailing
    whitespace stripped). Lines before the first `## ` header are dropped --
    idea cards have no meaningful content there.
    """
    sections: dict[str, list[tuple[int, str]]] = {}
    current_title: str | None = None
    for lineno, text in lines:
        match = TOP_HEADER_RE.match(text)
        if match:
            current_title = match.group(1)
            sections.setdefault(current_title, [])
            continue
        if current_title is not None:
            sections[current_title].append((lineno, text))
    return sections


def split_claim_columns(claim_lines: list[tuple[int, str]]) -> dict[str, list[tuple[int, str]]]:
    """Split the `## Claim` body into its double-column subsections.

    Keys are normalized to `hypothesis` / `assertable`; `#### delta` and
    everything under it is filed under the separate key `delta` and must
    never be scanned by L1/L7 (delta legitimately cites competitors' specific
    numbers). Content appearing before any recognized subheading -- i.e. the
    whole `## Claim` body when neither double-column subheading exists yet --
    is filed under `_whole`, so L1 can degrade to scanning the entire Claim
    section when the double columns are missing (S1 reports the missing
    columns separately).
    """
    columns: dict[str, list[tuple[int, str]]] = {"_whole": []}
    current_key = "_whole"
    for lineno, text in claim_lines:
        if DELTA_HEADER_RE.match(text):
            current_key = "delta"
            columns.setdefault(current_key, [])
            continue
        if HYPOTHESIS_HEADER_RE.match(text):
            current_key = "hypothesis"
            columns.setdefault(current_key, [])
            continue
        if ASSERTABLE_HEADER_RE.match(text):
            current_key = "assertable"
            columns.setdefault(current_key, [])
            continue
        match = SUB_HEADER_RE.match(text)
        if match:
            # some other/unrecognized ### subheading -- keep it isolated
            # under its own raw title so it never leaks into hypothesis /
            # assertable / delta scans.
            current_key = match.group(1)
            columns.setdefault(current_key, [])
            continue
        columns[current_key].append((lineno, text))

    if not columns["_whole"]:
        del columns["_whole"]
    return columns


def card_type(fm_text: str) -> str | None:
    """Classify a card by its frontmatter `type:`/`kind:`/`maintainer:` field.

    Returns "idea" for `type: idea`, "direction" for `type: direction`,
    "goal" for `kind: adopted-goal`, "field" for `maintainer:
    wiki-cartographer` (field files have no `type:` key -- see
    FIELD_MAINTAINER_RE's note), and None for anything else (files with no
    recognizable stamp at all stay silently skipped, exactly as before).

    The frontmatter keys are checked independently and never fall back to
    one another: a card missing all of them stays classified as "not a
    target card, skip" -- it must NOT be treated as an error (see
    05-RESEARCH.md Design Extraction §2, "kind: adopted-goal ... 不是第五种
    note 型").
    """
    if IDEA_TYPE_RE.search(fm_text):
        return "idea"
    if DIRECTION_TYPE_RE.search(fm_text):
        return "direction"
    if GOAL_KIND_RE.search(fm_text):
        return "goal"
    if FIELD_MAINTAINER_RE.search(fm_text):
        return "field"
    return None


def is_idea_card(fm_text: str) -> bool:
    """True only for cards whose frontmatter declares `type: idea`.

    Thin backward-compatible wrapper around card_type() -- kept so any
    existing call site keeps working silently instead of breaking when the
    single is_idea_card() check was generalized into card_type() dispatch
    (see 04-RESEARCH.md Pitfall #8).
    """
    return card_type(fm_text) == "idea"


# ---------------------------------------------------------------------------
# Violations & reporting
# ---------------------------------------------------------------------------


@dataclass
class Violation:
    path: Path
    line: int
    rule: str
    message: str


def report(violations: list[Violation]) -> None:
    for violation in violations:
        print(f"{violation.path}:{violation.line}: [{violation.rule}] {violation.message}")


# ---------------------------------------------------------------------------
# Rules (S1/L1 filled in by 03-02 Task 2; L2/L3/L4/L7 filled in by Task 3).
# Each rule function returns a list of (line, message) tuples; lint_file()
# tags them with the rule id and wraps them into Violation objects.
#
# NOTE: L5/L6/hedge judgment-backing/pivot-gradient-budget are intentionally
# deferred out of this milestone -- see the module docstring's "Deferred"
# section for the full list and its rationale.
# ---------------------------------------------------------------------------

# S1: an Observation opening line starting with any of these (after stripping
# a leading "[w]"/"[p]"/"[e]" anchor tag and bullet markers) means the card is
# still proposing/designing rather than reporting an observed anchor.
PROPOSE_DESIGN_RE = re.compile(r"^(propose|design|提出)", re.IGNORECASE)
ANCHOR_TAG_RE = re.compile(r"^\[[wpe]\]\s*")

# L1 over-specification pattern set (宁窄勿宽 -- no generic \d+ catch-all is
# permitted; every pattern below is a named, narrowly-scoped constant so
# future phases can extend the set without guessing at intent).
PARAM_UNIT = re.compile(r"\d[\d,.]*\s*[BM]\b")
CN_MEASURE = re.compile(r"\d[\d,]*\s*(?:例|个|条|篇|台|卡|张|轮|次)")
ARXIV_ID = re.compile(r"\b\d{4}\.\d{4,5}\b")
MODEL_NAME = re.compile(r"\b(?:GPT-|Llama|Qwen|Mistral|Gemma)\w*")
BENCH_NAME = re.compile(r"\bon\s+[A-Z]\w*[Bb]ench\w*")

L1_PATTERNS = (PARAM_UNIT, CN_MEASURE, ARXIV_ID, MODEL_NAME, BENCH_NAME)


def _first_line_of(lines: list[tuple[int, str]], default: int = 1) -> int:
    return lines[0][0] if lines else default


def _first_nonblank(lines: list[tuple[int, str]]) -> tuple[int, str] | None:
    for lineno, text in lines:
        if text.strip():
            return lineno, text
    return None


def rule_s1_structure(
    sections: dict[str, list[tuple[int, str]]],
    claim_columns: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []

    for name in TOP_SECTIONS:
        if name not in sections:
            violations.append((1, f"缺少顶层节 `## {name}`"))

    if "Observation" in sections:
        obs_lines = sections["Observation"]
        first = _first_nonblank(obs_lines)
        if first is None:
            violations.append((_first_line_of(obs_lines), "`## Observation` 正文为空"))
        else:
            lineno, text = first
            stripped = text.strip().lstrip("-*").strip()
            stripped = ANCHOR_TAG_RE.sub("", stripped)
            if PROPOSE_DESIGN_RE.match(stripped):
                violations.append(
                    (lineno, "`## Observation` 正文以 propose/design/提出 开头")
                )

    if "Claim" in sections:
        claim_lines = sections["Claim"]
        has_hypothesis = "hypothesis" in claim_columns
        has_assertable = "assertable" in claim_columns
        if not has_hypothesis:
            violations.append(
                (_first_line_of(claim_lines), "`## Claim` 缺 `### Hypothesis(大胆版)` 双栏子标题")
            )
        if not has_assertable:
            violations.append(
                (_first_line_of(claim_lines), "`## Claim` 缺 `### 当前可断言(assertable now)` 双栏子标题")
            )
        if has_hypothesis:
            hyp_lines = claim_columns["hypothesis"]
            hyp_text = "\n".join(text for _, text in hyp_lines)
            if "Reframe:" not in hyp_text:
                violations.append(
                    (
                        _first_line_of(hyp_lines, _first_line_of(claim_lines)),
                        "`### Hypothesis(大胆版)` 栏缺 `Reframe:` 句",
                    )
                )

    return violations


# S2: frontmatter `status:`/`residual_destination:` are read from the flat
# top-level lines only -- the regexes anchor at line-start (no leading
# whitespace), so a same-named key nested under `execution:`/`interest:`
# (neither of which currently has one, but future fields might) can never
# false-positive. `status:` intentionally is not `(?m)`-multiline-matched
# across the whole frontmatter blob the way IDEA_TYPE_RE etc. are -- S2 walks
# `fm_lines` one line at a time so it can also recover the line number, which
# a whole-blob regex on `fm_text` cannot.
STATUS_LINE_RE = re.compile(r"^status:\s*(.*?)\s*$")
RESIDUAL_DESTINATION_LINE_RE = re.compile(r"^residual_destination:\s*(.*?)\s*$")

# Only these two status values require a filled residual_destination (see
# docs/llm-wiki.protocol.yaml idea_lifecycle.residual_destination_rule).
RESIDUAL_REQUIRED_STATUSES = ("RETIRED", "PARKED")


def rule_s2_residual_destination(
    fm_lines: list[tuple[int, str]],
) -> list[tuple[int, str]]:
    """`status: RETIRED` or `status: PARKED` requires a non-empty
    `residual_destination` -- see idea_lifecycle.residual_destination_rule.

    A missing key, `null`, an empty string (`""`/`''`), or a whitespace-only
    value all count as "missing". Any other `status:` value is left alone
    (S2 reports nothing). When `residual_destination:` is present at all
    (even if its value is missing), the violation anchors to that line --
    easier to fix than pointing back up at `status:`; only a wholly absent
    key falls back to the `status:` line.
    """
    status_line: int | None = None
    status_value: str | None = None
    residual_line: int | None = None
    residual_value: str | None = None

    for lineno, text in fm_lines:
        if status_line is None:
            match = STATUS_LINE_RE.match(text)
            if match:
                status_line = lineno
                status_value = match.group(1)
                continue
        if residual_line is None:
            match = RESIDUAL_DESTINATION_LINE_RE.match(text)
            if match:
                residual_line = lineno
                residual_value = match.group(1)

    if status_value not in RESIDUAL_REQUIRED_STATUSES:
        return []

    normalized = (residual_value or "").strip().strip("\"'").strip()
    is_missing = residual_value is None or normalized == "" or normalized == "null"
    if not is_missing:
        return []

    anchor_line = residual_line if residual_line is not None else status_line
    return [
        (
            anchor_line,
            f"status: {status_value} 但 residual_destination 缺失/为空 —— "
            "死亡/搁置必须填残值去向(指向 wiki/salvage/ 或某条 field 层记录:"
            "assumptions.md / tensions.md / saturation.md / problems.md)",
        )
    ]


def _scan_l1(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for lineno, text in lines:
        for pattern in L1_PATTERNS:
            for match in pattern.finditer(text):
                hits.append((lineno, match.group(0)))
    return hits


def rule_l1_overspecification(
    claim_columns: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []

    # Only the two double-column subsections are in scope; `delta` is never
    # scanned (see split_claim_columns docstring). When neither column
    # subheading exists yet, degrade to scanning the whole `## Claim` body
    # (still excluding delta) -- S1 reports the missing columns separately.
    scan_keys = [key for key in ("hypothesis", "assertable") if key in claim_columns]
    if not scan_keys and "_whole" in claim_columns:
        scan_keys = ["_whole"]

    for key in scan_keys:
        for lineno, hit in _scan_l1(claim_columns[key]):
            violations.append(
                (lineno, f"Claim 双栏出现具体实例参数「{hit}」—— 移入 Instantiation 并标 [default]")
            )

    return violations


DOF_TAGS = ("[load-bearing]", "[default]", "[free]")


def rule_l2_dof(sections: dict[str, list[tuple[int, str]]]) -> list[tuple[int, str]]:
    """Every Instantiation & DoF setting line (starts with -/* and has a
    colon) must carry one of the three DoF tags. Table headers, blank lines,
    and plain prose lines are not setting lines and are skipped naturally
    because they don't match the "-/* ... :" shape.
    """
    violations: list[tuple[int, str]] = []
    for lineno, text in sections.get("Instantiation & DoF", []):
        stripped = text.strip()
        if not stripped:
            continue
        if not (stripped.startswith("-") or stripped.startswith("*")):
            continue
        if ":" not in stripped and "：" not in stripped:
            continue
        if not any(tag in stripped for tag in DOF_TAGS):
            violations.append(
                (lineno, "Instantiation 设定行缺少 DoF 标注([load-bearing]/[default]/[free])")
            )
    return violations


DERIVATION_RE = re.compile(r"[\(（]推导[:：]")


def rule_l3_load_bearing(sections: dict[str, list[tuple[int, str]]]) -> list[tuple[int, str]]:
    """Every [load-bearing] line must be followed (same line or the very next
    line) by a "(推导: ...)" sentence.
    """
    violations: list[tuple[int, str]] = []
    lines = sections.get("Instantiation & DoF", [])
    for idx, (lineno, text) in enumerate(lines):
        if "[load-bearing]" not in text:
            continue
        has_derivation = bool(DERIVATION_RE.search(text))
        if not has_derivation and idx + 1 < len(lines):
            has_derivation = bool(DERIVATION_RE.search(lines[idx + 1][1]))
        if not has_derivation:
            violations.append(
                (lineno, "[load-bearing] 行缺少「(推导: …)」一句 —— 写不出请降为 [default]")
            )
    return violations


PIVOT_RULE_RE = re.compile(r"^\s*[-*]?\s*R\d+\s*[:：]")


def rule_l4_pivot(sections: dict[str, list[tuple[int, str]]]) -> list[tuple[int, str]]:
    """`## Pivot rules` must list at least 2 `R<n>:` rules (no experimental
    redundancy otherwise)."""
    lines = sections.get("Pivot rules", [])
    count = sum(1 for _, text in lines if PIVOT_RULE_RE.match(text))
    if count < 2:
        return [(_first_line_of(lines), f"pivot 规则仅 {count} 条(需 >=2)—— 无实验冗余")]
    return []


# hedge/qualifier word list -- NOT imported from paper-de-defense/defense_scan.py
# (that word list is English-only, tuned for academic prose polish). This is a
# new, deliberately small中英混排 list assembled from the three source
# passages cited in 03-RESEARCH.md Pitfall #10 (design1 L7 / design3 C5(b) /
# design2 comp5(d)). Sorted longest-first so the alternation regex prefers
# the longer phrase over a shorter substring it contains (e.g. "可能仅" over
# a bare "可能").
HEDGE_TERMS = [
    "we do not claim",
    "under certain",
    "in some settings",
    "preliminary",
    "在某些情况下",
    "可能仅",
    "只是初探",
    "不声称超越",
    "作为补充",
    "might",
    "may",
    "可能",
    "初步",
]
HEDGE_RE = re.compile("|".join(re.escape(term) for term in HEDGE_TERMS), re.IGNORECASE)

# canonical Hypothesis template fixed phrase -- stripped out of the scanned
# text before counting hedge hits, so a compliant card using the template
# verbatim is not flagged by its own boilerplate.
TEMPLATE_CARVEOUTS = ["机制上可能源于"]


def rule_l7_hedge(claim_columns: dict[str, list[tuple[int, str]]]) -> list[tuple[int, str]]:
    keys = [key for key in ("hypothesis", "assertable") if key in claim_columns]
    if not keys and "_whole" in claim_columns:
        keys = ["_whole"]
    if not keys:
        return []

    combined = "\n".join(text for key in keys for _, text in claim_columns[key])
    for carveout in TEMPLATE_CARVEOUTS:
        combined = combined.replace(carveout, "")

    hits: list[str] = []
    seen_norm: set[str] = set()
    seen_order: list[str] = []
    for match in HEDGE_RE.finditer(combined):
        term = match.group(0)
        hits.append(term)
        norm = term.lower()
        if norm not in seen_norm:
            seen_norm.add(norm)
            seen_order.append(term)

    if len(hits) > 2:
        first_lineno = _first_line_of(claim_columns[keys[0]])
        return [
            (
                first_lineno,
                f"Claim 双栏 hedge 限定词 {len(hits)} 个(上限 2):{'、'.join(seen_order)}",
            )
        ]
    return []


# ---------------------------------------------------------------------------
# C2/C3 (idea cards only): assertable-column overclaim ceiling + [p:] probe
# reference indicative-marker check.
#
# NOTE on notation: vendor prose calls the three evidence-strength tiers
# A0/A1/A2, but `## Attributability preconditions` already uses `A1:`/`A2:`/
# `A3:` as an entry-numbering prefix (rule_l3_load_bearing depends on that
# numbering). To avoid grep/visual collision, A0/A1/A2 notation is used only
# in prose/identifiers here -- the bare tier number is never followed by a
# colon and printed as a card-text or lint-message prefix.
# ---------------------------------------------------------------------------

# Anchor tag at the start of an `## Observation` entry line (bullet-prefixed
# variant of ANCHOR_TAG_RE, which is the no-bullet version S1 uses on the
# section's first line). Kept as an independent constant -- do not merge
# with ANCHOR_TAG_RE.
OBS_ANCHOR_RE = re.compile(r"^\s*[-*]\s*\[([wpe])\]")

_ANCHOR_RANK = {"w": 0, "p": 1, "e": 2}

# A1-tier (indicative) language -- allowed once the evidence ceiling has
# climbed to [p]. Seed list, not sealed -- may be appended to later.
INDICATIVE_TERMS = [
    "初步显示",
    "趋势提示",
    "初步观察到",
    "indicative",
    "preliminary evidence suggests",
]
INDICATIVE_RE = re.compile(
    "|".join(re.escape(term) for term in sorted(INDICATIVE_TERMS, key=len, reverse=True)),
    re.IGNORECASE,
)

# A2-tier (assertion) language -- v0's evidence ceiling can never reach [e],
# so any hit here is a violation regardless of anchor state. Seed list, not
# sealed -- may be appended to later.
ASSERTION_TERMS = [
    "证明",
    "证实",
    "结果表明",
    "表明",
    "建立了",
    "we show that",
    "we demonstrate that",
    "we prove that",
]
ASSERTION_RE = re.compile(
    "|".join(re.escape(term) for term in sorted(ASSERTION_TERMS, key=len, reverse=True)),
    re.IGNORECASE,
)

PROBE_REF_RE = re.compile(r"\[p:\s*[^\]]+\]")

# A pure placeholder line ("<...>") does not count as substantive assertable
# prose for the C2 "无锚断言句" branch.
PLACEHOLDER_LINE_RE = re.compile(r"^<.*>$")


def evidence_ceiling(sections: dict[str, list[tuple[int, str]]]) -> tuple[str, bool]:
    """Scan `## Observation` entry lines for their leading anchor tag.

    Returns (ceiling, has_any_anchor): ceiling is the highest-lifecycle
    anchor seen ([w] < [p] < [e]); when no anchor is present at all, ceiling
    defaults to "w" and has_any_anchor is False, so callers can tell "capped
    at [w] because that's the highest anchor present" apart from "capped at
    [w] because there is no anchor at all" (the latter is the separate C2
    无锚断言句 branch). Does not cross-read probes/ledger.jsonl -- v0 stays
    single-file (see 04-RESEARCH.md Design Extraction §3a).
    """
    best_rank = -1
    best_tag: str | None = None
    for _, text in sections.get("Observation", []):
        match = OBS_ANCHOR_RE.match(text)
        if not match:
            continue
        tag = match.group(1)
        rank = _ANCHOR_RANK[tag]
        if rank > best_rank:
            best_rank = rank
            best_tag = tag
    if best_tag is None:
        return "w", False
    return best_tag, True


def rule_c2_evidence_ceiling(
    sections: dict[str, list[tuple[int, str]]],
    claim_columns: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []

    # Only the assertable column is in scope; when it's missing, degrade to
    # `_whole` (same fallback shape as L1/L7). `delta` is never scanned.
    if "assertable" in claim_columns:
        scan_lines = claim_columns["assertable"]
    elif "_whole" in claim_columns:
        scan_lines = claim_columns["_whole"]
    else:
        scan_lines = []

    ceiling, has_anchor = evidence_ceiling(sections)

    if ceiling == "e":
        # A self-written [e] anchor is itself a violation: no experiment
        # ledger exists in v0 that could certify it (see C4 in the Deferred
        # list). Anchor the violation to the [e] line under `## Observation`
        # (falling back to the section's first line), then continue the
        # assertion scan as if the ceiling were [p] so overclaim stays gated.
        obs_lines = sections.get("Observation", [])
        anchor_line = _first_line_of(obs_lines)
        for lineno, text in obs_lines:
            match = OBS_ANCHOR_RE.match(text)
            if match and match.group(1) == "e":
                anchor_line = lineno
                break
        violations.append(
            (
                anchor_line,
                "[e] anchor cannot be produced in v0 (no experiment ledger "
                "exists); a self-written [e] is invalid -- evidence ceiling "
                "treated as [p]",
            )
        )
        ceiling = "p"

    if ceiling == "w":
        active_patterns = (INDICATIVE_RE, ASSERTION_RE)
    else:  # "p" -- including a rejected [e] downgraded just above
        active_patterns = (ASSERTION_RE,)

    for lineno, text in scan_lines:
        earliest = None
        for pattern in active_patterns:
            match = pattern.search(text)
            if match and (earliest is None or match.start() < earliest.start()):
                earliest = match
        if earliest is not None:
            violations.append(
                (
                    lineno,
                    f"assertable 栏断言强度超出证据等级上限(当前上限 [{ceiling}]):「{earliest.group(0)}」",
                )
            )

    if not has_anchor:
        has_substantive = any(
            text.strip() and not PLACEHOLDER_LINE_RE.match(text.strip())
            for _, text in scan_lines
        )
        if has_substantive:
            violations.append(
                (
                    _first_line_of(scan_lines),
                    "assertable 栏出现无锚断言句(Observation 无任何 [w]/[p]/[e] 锚)",
                )
            )

    return violations


def rule_c3_indicative_marker(
    claim_columns: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []
    for lineno, text in claim_columns.get("assertable", []):
        if not PROBE_REF_RE.search(text):
            continue
        if INDICATIVE_RE.search(text):
            continue
        violations.append((lineno, f"[p:] 引用缺 indicative 标记:{text.strip()}"))
    return violations


# T1 (idea cards only): frontmatter `important_problem:` line, matched with
# leading whitespace allowed because the key nests under the `interest:`
# block. First hit wins -- idea cards carry exactly one such line.
IMPORTANT_PROBLEM_LINE_RE = re.compile(r"^\s*important_problem:\s*(.*?)\s*$")


def _wikilink_target(link: str) -> str:
    """Normalize a full `[[...]]` match to its bare target: strip the
    brackets, then a `|alias` tail, then a `#fragment` tail."""
    inner = link[2:-2]
    inner = inner.split("|", 1)[0]
    inner = inner.split("#", 1)[0]
    return inner.strip()


def _wiki_instance_root(path: Path) -> Path | None:
    """Locate the wiki instance root: walk path.resolve().parents for a
    component named 'wiki' and return its parent directory. Returns None
    when no 'wiki' component exists -- the fixture-compatibility keystone:
    production idea cards always live under wiki/ideas/ so the root always
    resolves; examples/ cards outside any wiki/ tree skip the existence
    check and keep their pre-T1 verdicts.
    """
    for parent in path.resolve().parents:
        if parent.name == "wiki":
            return parent.parent
    return None


def rule_t1_important_problem(
    path: Path,
    fm_lines: list[tuple[int, str]],
) -> list[tuple[int, str]]:
    """Non-empty `important_problem` must anchor via `[[链接]]`, and every
    link target must exist on disk (与既有 dangling 检查同构). Empty/null
    values are out of scope -- interest 五键非空才算数,空值本来就自动排除
    出顶会档(protocol `idea_tiering.interest_questions.important_problem`),
    T1 只管「非空但挂靠是假的」这一偷懒面(方案§三·5 谓词③,堵乙13)。
    """
    hit: tuple[int, str] | None = None
    for lineno, text in fm_lines:
        match = IMPORTANT_PROBLEM_LINE_RE.match(text)
        if match:
            hit = (lineno, match.group(1))
            break
    if hit is None:
        return []

    lineno, raw_value = hit
    value = raw_value.strip().strip("\"'").strip()
    if value == "" or value == "null":
        return []

    links = WIKILINK_RE.findall(raw_value)
    if not links:
        return [
            (
                lineno,
                "important_problem 非空但未以 [[链接]] 挂靠——挂靠必须指向"
                "真实 field 层记录",
            )
        ]

    instance_root = _wiki_instance_root(path)
    if instance_root is None:
        return []

    violations: list[tuple[int, str]] = []
    for link in links:
        target = _wikilink_target(link)
        if "/" in target or target.endswith(".md"):
            rel = target if target.endswith(".md") else target + ".md"
            exists = (instance_root / rel).is_file()
        else:
            exists = any((instance_root / "wiki").rglob(f"{target}.md"))
        if not exists:
            violations.append(
                (
                    lineno,
                    f"important_problem 挂靠目标不存在:[[{target}]]"
                    "(与 dangling 检查同构)",
                )
            )
    return violations


# ---------------------------------------------------------------------------
# D1 (direction cards only): interrogative direction statement + four-section
# skeleton. This rule set is disjoint from the idea-card rules above -- a
# direction card never runs S1/S2/L1/L2/L3/L4/L7/C2/C3, and an idea card
# never runs D1 (see lint_file()'s dispatch).
# ---------------------------------------------------------------------------


def _looks_like_disguised_hypothesis(text: str) -> bool:
    """True when `text` co-occurs the idea-card Hypothesis template's core
    verb phrase ("存在"/"表现出" together with "机制上可能源于") -- i.e. it
    reads like a mechanism-attribution declarative sentence dressed up as a
    direction statement. Deliberately narrow (宁窄勿宽): no broader semantic
    judgement is attempted here.
    """
    has_verb = ("存在" in text) or ("表现出" in text)
    has_mechanism = "机制上可能源于" in text
    return has_verb and has_mechanism


def rule_d1_interrogative(sections: dict[str, list[tuple[int, str]]]) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []

    for name in DIRECTION_SECTIONS:
        if name not in sections:
            violations.append((1, f"方向卡缺少节「{name}」"))

    if "方向陈述" in sections:
        first = _first_nonblank(sections["方向陈述"])
        if first is not None:
            lineno, text = first
            stripped = text.strip()
            ends_with_question = stripped.endswith("？") or stripped.endswith("?")
            if not ends_with_question:
                message = f"方向陈述必须以问号结尾(禁机制归因命题句):{stripped}"
                if _looks_like_disguised_hypothesis(stripped):
                    message += " —— 疑似 idea 卡 Hypothesis 句伪装成方向卡"
                violations.append((lineno, message))

    return violations


# ---------------------------------------------------------------------------
# G1-G6 (goal cards only): the six machine-checkable goal-card constraints.
# This rule set is disjoint from the idea-card and direction-card rules
# above -- a goal card never runs S1/S2/L1/.../C3/D1, and idea/direction
# cards never run G1-G6 (see lint_file()'s dispatch). See the module docstring's
# "G1-G6 provenance" note for the honest [ASSUMED] flag on this rule set.
# ---------------------------------------------------------------------------

# G1 method-name ban word list -- reuses/extends the idea-card Hypothesis
# column's over-specification word list (MODEL_NAME, defined above for L1)
# with generic method-name terms. 宁窄勿宽 -- named, narrow terms only; not
# sealed, may be appended to later (same policy as HEDGE_TERMS/L1_PATTERNS).
GOAL_METHOD_TERMS = [
    "contrastive learning",
    "fine-tuning",
    "prompt engineering",
    "knowledge distillation",
    "reinforcement learning",
    "diffusion model",
    "对比学习",
    "微调",
    "提示工程",
    "知识蒸馏",
    "强化学习",
    "扩散模型",
    "注意力机制",
]
GOAL_METHOD_RE = re.compile(
    "|".join(re.escape(term) for term in sorted(GOAL_METHOD_TERMS, key=len, reverse=True)),
    re.IGNORECASE,
)

# "用 X 解决" / "通过 X 解决" -- the solve-sentence pattern that writes the
# solution into the problem statement (vendor: 「用 X 解决」句式).
METHOD_SOLVE_RE = re.compile(r"(?:用|通过)[^。,，\n]{0,30}解决")

# G2/G3 facet tag, e.g. `[facet: main]` / `[facet: heldout]` / `[facet:
# mechanism]` -- verbatim from WIKI.md.tmpl §4e's Success criteria example.
FACET_RE = re.compile(r"\[facet:\s*(main|heldout|mechanism)\]")
GOAL_FACETS = ("main", "heldout", "mechanism")

# G3 heldout-object real-name word list -- a seed set of well-known
# benchmark/dataset proper names (word-list method, same policy as
# GOAL_METHOD_TERMS: not sealed, may be appended to later). BENCH_NAME
# (defined above for L1) is reused alongside this list, matching the
# "on XBench"-shaped generic case this list's literal names don't cover.
GOAL_DATASET_TERMS = [
    "ImageNet",
    "COCO",
    "GLUE",
    "SQuAD",
    "MMLU",
    "GSM8K",
    "HumanEval",
    "SWE-bench",
    "HellaSwag",
    "TruthfulQA",
    "CIFAR-10",
    "WMT14",
]
GOAL_DATASET_RE = re.compile(
    "|".join(re.escape(term) for term in sorted(GOAL_DATASET_TERMS, key=len, reverse=True)),
    re.IGNORECASE,
)

# G4/G5/G6 wikilink pattern -- a *complete* `[[id]]` link anywhere in the
# line (deliberately not anchored to line-start, unlike test_contracts.py's
# WIKILINK which validates a field value string in isolation).
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")

# G4 anchor-tag pattern -- the same `[w]`/`[p]`/`[e]` anchor syntax direction
# cards' Wedges use (see examples/probe-layer-fixtures's Wedges bullets: "-
# [w] ... 链到某表格"). Reuses the OBS_ANCHOR_RE tag shape but is not
# anchored to the start of the line/bullet the way OBS_ANCHOR_RE is, because
# Admissibility bullets place the anchor after the ban clause (see
# WIKI.md.tmpl §4e: "- 禁止 <...> —— 锚 [[wiki 证据]]").
ANCHOR_TAG_ANY_RE = re.compile(r"\[[wpe]\]")

# G5 partially-solved carve-out marker -- a bullet claiming this must carry
# a ledger-entry wikilink (checked separately via WIKILINK_RE).
NON_GOAL_PARTIAL_TERMS = ("partially-solved", "部分解决")


def rule_g1_problem_statement(
    sections: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    """`## 问题陈述` must not name a method or use a "用 X 解决" solve
    sentence -- goal-period method novelty (Heilmeier Q3) is deferred to
    direction cards. A missing section is itself a violation.
    """
    lines = sections.get(GOAL_SEC_PROBLEM, [])
    if not lines:
        return [(1, f"goal 卡缺少 `## {GOAL_SEC_PROBLEM}` 节")]

    violations: list[tuple[int, str]] = []
    for lineno, text in lines:
        if not text.strip():
            continue
        hits: list[str] = []
        for pattern in (GOAL_METHOD_RE, MODEL_NAME):
            match = pattern.search(text)
            if match:
                hits.append(match.group(0))
        solve_match = METHOD_SOLVE_RE.search(text)
        if solve_match:
            hits.append(solve_match.group(0))
        for hit in hits:
            violations.append(
                (
                    lineno,
                    f"问题陈述出现方法名/解法句式「{hit}」—— goal 期禁方法名"
                    "(Heilmeier Q3 下放 direction 卡)",
                )
            )
    return violations


def rule_g2_facet_coverage(
    sections: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    """`## Success criteria` must carry >= 1 entry for each of
    main/heldout/mechanism (missing section degrades to "all three
    missing", same shape as an empty section).
    """
    lines = sections.get(GOAL_SEC_SUCCESS_CRITERIA, [])
    found: set[str] = set()
    for _, text in lines:
        match = FACET_RE.search(text)
        if match:
            found.add(match.group(1))
    missing = [facet for facet in GOAL_FACETS if facet not in found]
    if missing:
        return [
            (
                _first_line_of(lines),
                f"Success criteria facet 缺失: {'/'.join(missing)}"
                "(main/heldout/mechanism 各需 >=1 条)",
            )
        ]
    return []


def rule_g3_heldout_no_realname(
    sections: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    """Entries tagged `[facet: heldout]` must not name a concrete
    dataset/benchmark -- goal period bans naming the heldout object (the
    object is drawn by the method-blind party at experiment time).
    """
    violations: list[tuple[int, str]] = []
    for lineno, text in sections.get(GOAL_SEC_SUCCESS_CRITERIA, []):
        match = FACET_RE.search(text)
        if not match or match.group(1) != "heldout":
            continue
        hits: list[str] = []
        for pattern in (GOAL_DATASET_RE, BENCH_NAME):
            hit = pattern.search(text)
            if hit:
                hits.append(hit.group(0))
        for hit in hits:
            violations.append(
                (
                    lineno,
                    f"heldout facet 条目出现实名数据集/benchmark「{hit}」"
                    "—— goal 期禁实名(实验期由方法盲的一方抽取)",
                )
            )
    return violations


def rule_g4_admissibility_anchor(
    sections: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    """Every `## Admissibility` bullet must carry a `[[wikilink]]` or a
    `[w]`/`[p]`/`[e]` anchor tag -- the same anchor syntax direction cards'
    Wedges use. A missing section is itself a violation.
    """
    lines = sections.get(GOAL_SEC_ADMISSIBILITY, [])
    if not lines:
        return [(1, f"goal 卡缺少 `## {GOAL_SEC_ADMISSIBILITY}` 节")]

    violations: list[tuple[int, str]] = []
    for lineno, text in lines:
        stripped = text.strip()
        if not stripped or not (stripped.startswith("-") or stripped.startswith("*")):
            continue
        if WIKILINK_RE.search(stripped) or ANCHOR_TAG_ANY_RE.search(stripped):
            continue
        violations.append(
            (
                lineno,
                "Admissibility 条目缺锚(需 [[wikilink]] 或 [w]/[p]/[e] 锚标签"
                "—— 与方向卡 Wedges 同一套锚语法)",
            )
        )
    return violations


def rule_g5_non_goals(
    sections: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    """`## Non-goals` must not be empty; any bullet claiming a
    partially-solved carve-out must carry a `[[ledger 条目]]` wikilink.
    """
    lines = sections.get(GOAL_SEC_NON_GOALS, [])
    items = [
        (lineno, text)
        for lineno, text in lines
        if text.strip() and (text.strip().startswith("-") or text.strip().startswith("*"))
    ]
    if not items:
        return [
            (
                _first_line_of(lines),
                f"`## {GOAL_SEC_NON_GOALS}` 节为空 —— partially-solved 划走的子集须逐条带引用,"
                "禁止空节",
            )
        ]

    violations: list[tuple[int, str]] = []
    for lineno, text in items:
        if any(term in text for term in NON_GOAL_PARTIAL_TERMS) and not WIKILINK_RE.search(text):
            violations.append(
                (lineno, "Non-goals 条目声明 partially-solved 划走但缺 [[ledger 条目]] 引用")
            )
    return violations


def rule_g6_attack_surface(
    sections: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    """`## Attack surface` must carry >= 2 `[[wikilink]]` entries."""
    lines = sections.get(GOAL_SEC_ATTACK_SURFACE, [])
    count = sum(len(WIKILINK_RE.findall(text)) for _, text in lines)
    if count < 2:
        return [
            (
                _first_line_of(lines),
                f"`## {GOAL_SEC_ATTACK_SURFACE}` 仅 {count} 个 [[wikilink]]"
                "(需 >=2 件,逐件核实存在且已读)",
            )
        ]
    return []


# ---------------------------------------------------------------------------
# F1 (field files only): per-entry citation count + distinct-target dedup.
# Field files are dispatched by their `maintainer: wiki-cartographer` stamp
# (FIELD_MAINTAINER_RE) -- they run F1 and nothing else. Goal cards are
# explicitly exempt (`kind: adopted-goal` dispatches to the G branch,
# matching protocol `goal 卡 grounding: "not subject to field's >=3-paper
# claim rule"`); a `problems.md` one-line candidate list carries no
# frontmatter stamp and no `## ` entries, so it trips nothing.
# ---------------------------------------------------------------------------


def rule_f1_citations(
    sections: dict[str, list[tuple[int, str]]],
) -> list[tuple[int, str]]:
    """Every `## ` entry of a field file must carry >= 3 `[[引用]]` links
    (agents/wiki-cartographer.md '3-paper bar' 从 prompt 级搬到输出级,堵
    乙15) pointing to >= 2 distinct targets after stripping `|alias` and
    `#fragment` (红队#5 补法,封「引同一篇三次凑数」). Violations anchor to
    the entry's first line.
    """
    violations: list[tuple[int, str]] = []
    for _, lines in sections.items():
        links: list[str] = []
        for _, text in lines:
            links.extend(WIKILINK_RE.findall(text))
        n = len(links)
        distinct = len({_wikilink_target(link) for link in links})
        anchor = _first_line_of(lines)
        if n < 3:
            violations.append(
                (anchor, f"field 条目 [[引用]] 仅 {n} 条(需 ≥3 篇 wiki 论文出处)")
            )
        if distinct < 2:
            violations.append(
                (
                    anchor,
                    f"field 条目 [[引用]] 去重后仅指向 {distinct} 个目标"
                    "(需 ≥2 个不同目标)",
                )
            )
    return violations


def lint_file(
    path: Path,
    fm_text: str,
    fm_lines: list[tuple[int, str]],
    body_lines: list[tuple[int, str]],
) -> list[Violation]:
    sections = split_sections(body_lines)
    card = card_type(fm_text)

    tagged: list[tuple[int, str, str]] = []

    if card == "direction":
        for line, message in rule_d1_interrogative(sections):
            tagged.append((line, "D1", message))
    elif card == "goal":
        # G1-G6 rule bodies filled in below (05-03 Task 2); this branch is
        # intentionally disjoint from the idea/direction branches -- a goal
        # card never runs S1/S2/L1/.../C3/D1, and idea/direction cards never
        # run G1-G6.
        for line, message in rule_g1_problem_statement(sections):
            tagged.append((line, "G1", message))
        for line, message in rule_g2_facet_coverage(sections):
            tagged.append((line, "G2", message))
        for line, message in rule_g3_heldout_no_realname(sections):
            tagged.append((line, "G3", message))
        for line, message in rule_g4_admissibility_anchor(sections):
            tagged.append((line, "G4", message))
        for line, message in rule_g5_non_goals(sections):
            tagged.append((line, "G5", message))
        for line, message in rule_g6_attack_surface(sections):
            tagged.append((line, "G6", message))
    elif card == "field":
        # Field files run F1 only -- never the idea/direction/goal sets
        # (field 条目是台账行不是卡,九节骨架/双栏纪律对它没有意义).
        for line, message in rule_f1_citations(sections):
            tagged.append((line, "F1", message))
    else:
        claim_columns = split_claim_columns(sections.get("Claim", []))
        for line, message in rule_s1_structure(sections, claim_columns):
            tagged.append((line, "S1", message))
        for line, message in rule_s2_residual_destination(fm_lines):
            tagged.append((line, "S2", message))
        for line, message in rule_l1_overspecification(claim_columns):
            tagged.append((line, "L1", message))
        for line, message in rule_l2_dof(sections):
            tagged.append((line, "L2", message))
        for line, message in rule_l3_load_bearing(sections):
            tagged.append((line, "L3", message))
        for line, message in rule_l4_pivot(sections):
            tagged.append((line, "L4", message))
        for line, message in rule_l7_hedge(claim_columns):
            tagged.append((line, "L7", message))
        for line, message in rule_c2_evidence_ceiling(sections, claim_columns):
            tagged.append((line, "C2", message))
        for line, message in rule_c3_indicative_marker(claim_columns):
            tagged.append((line, "C3", message))
        for line, message in rule_t1_important_problem(path, fm_lines):
            tagged.append((line, "T1", message))

    # stable sort keeps the pass order (S1->S2->L1->L2->L3->L4->L7->C2->C3->
    # T1, or D1 alone, or G1->G2->G3->G4->G5->G6, or F1 alone) for ties on
    # the same line number.
    tagged.sort(key=lambda item: item[0])
    return [Violation(path, line, rule, message) for line, rule, message in tagged]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def collect_paths(arg: str) -> list[Path]:
    """Resolve a single CLI path argument to a sorted list of `.md` files.

    A file argument is returned as-is; a directory argument is scanned
    recursively (`rglob('*.md')`) and returned sorted. A nonexistent path
    exits the process immediately with code 2 (usage/IO error).
    """
    candidate = Path(arg)
    if candidate.is_file():
        return [candidate]
    if candidate.is_dir():
        return sorted(candidate.rglob("*.md"))
    print(f"error: path not found: {arg}", file=sys.stderr)
    sys.exit(2)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="idea_lint.py",
        description="Mechanical lint for paper-wiki idea cards (wiki/ideas/*.md).",
    )
    parser.add_argument(
        "path",
        nargs="+",
        help="idea card file(s) or directory(ies) to lint",
    )
    args = parser.parse_args(argv)

    all_paths: list[Path] = []
    for raw_arg in args.path:
        all_paths.extend(collect_paths(raw_arg))

    md_paths = sorted(set(all_paths))
    if not md_paths:
        print("error: no .md files found to lint", file=sys.stderr)
        sys.exit(2)

    violations: list[Violation] = []
    files_checked = 0
    files_skipped = 0
    for path in md_paths:
        fm_text, fm_lines, body_lines = read_card(path)
        if card_type(fm_text) is None:
            # A file that declares an explicit but unsupported `type:` (e.g.
            # a probe card) is announced and counted; files with no
            # recognizable type/kind at all stay silent.
            type_match = TYPE_LINE_RE.search(fm_text)
            if type_match:
                files_skipped += 1
                print(f"skipped (unsupported type: {type_match.group(1)}): {path}")
            continue
        files_checked += 1
        violations.extend(lint_file(path, fm_text, fm_lines, body_lines))

    report(violations)
    print(
        f"{len(violations)} violation(s) in {files_checked} file(s)"
        f" ({files_skipped} skipped)"
    )
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
