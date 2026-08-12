---
description: Search arXiv and the web for recent research papers, then offer a verified candidate list for import.
argument-hint: <topic / keywords>
---

Run the paper-wiki `wiki-search-latest` action. This file adapts the action to a
Claude Code slash command.

1. Read `WIKI.md` first, then `research.md` and the existing paper IDs under
   `wiki/papers/`.
2. Stop for a course wiki; outward paper search is research-only.
3. Respect `lifecycle_state`: stop when `FROZEN`; when `ACTIVE`, note that this
   explicit request is an on-demand expansion.
4. Resolve the search topic from the argument or current research focus. Ask if the
   intent is genuinely ambiguous.
5. Run the verified paper-search capability using the current scope fence and a
   24-month default window unless the user supplied another range.
6. Return at most ten candidates with verified identity/URL, relevance, date, and
   a `[FENCE]` marker for excluded areas. Deduplicate against compiled papers.
7. Ask the user which candidates to import. A recommendation is never permission
   to download or write into `raw/`.

   Auto-expansion branch — applies only when the instance sets
   `expansion_mode: auto` in `research.md` § Scope fence (default is
   `attended`, which keeps this step exactly as written above;
   `lifecycle_state: FROZEN` overrides every mode — step 3 already stops the
   run):
   - Eligible candidates are only those on the searcher's
     `## Recommended import priority` list — they already passed identity
     verification, dedup, and the scope fence. `[FENCE]` candidates never
     enter the recommended list and are never auto-imported.
   - Per-candidate confirmation is replaced by this standing policy. Every
     auto-import must record a `sponsor` (one of the six literals in protocol
     `library_expansion.triggers.sponsor_enum`, with the card/case id where
     applicable) — the accounting prerequisite for the count columns and the
     exempt marker. A candidate
     without a sponsor falls back to manual confirmation: not a violation,
     just never auto-imported.
   - Import triggers fall into exactly four classes: `manual` (attended
     only — never part of an auto run) / `bootstrap` (one-time
     post-first-compile whole-library round, cap-exempt) / `problem-card`
     (main engine — the only class the dual caps and the n/200 ratio
     count) / fallback (sponsors `openness-case` | `novelty-trial` |
     `needs-evidence`; library-query-first 查库→覆盖判断→缺料才出网,
     cap-exempt). Trigger semantics: protocol `library_expansion.triggers`.
   - Dual caps from `operational_parameters`（经验值(2026-08-12)，设计值可回调，
     终局归人）: `auto_import_run_max: 200` — cumulative cap per auto run,
     counting `problem-card` imports only;
     `auto_import_per_direction_lifetime: 10` — lifetime cap per
     problem-card (each card's quota, not a per-sponsor-class cap).
     When either cap is hit: stop problem-card auto expansion, write the
     termination line to the log, and fall back to `attended` for the rest
     of the run; the cap-exempt classes are unaffected by a cap hit.
   - Log every import — cap-exempt classes included — as one appended
     line in the instance's
     `raw/IMPORT-LOG.md` (append-only):
     `日期 | paper id | sponsor | 累计 n/200 | 该 sponsor m/10`; for the
     cap-exempt classes (`manual` / `bootstrap` / the three fallback
     sponsors) the count columns read `exempt` and the row does not count
     toward n/200. At run end
     append one total-ratio line `x/200`. A cap-hit line must state verbatim
     `run cap reached — expansion halted`.
   - Candidates released by this policy proceed to step 8 as approved.
8. After approval, fetch only the selected sources, verify identity again, and
   explain whether each is ready for the `wiki-compile` action or first needs GPU
   OCR.

`WIKI.md` is the only authoritative project rules file. Do not derive behavior
from `CLAUDE.md` or `AGENTS.md`. Do not let Claude Code and Codex write this
workspace concurrently.
