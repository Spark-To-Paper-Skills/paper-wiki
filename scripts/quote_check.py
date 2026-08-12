"""quote_check.py -- stdlib-only verbatim-quote existence check for the
novelty ledger.

The adjudication system's foundation is verbatim quotation: every quote a
charge cites in `wiki/novelty/ledger.md` is supposed to be a word-for-word
span of a compiled paper note. This script checks that each quoted span in
the ledger actually occurs somewhere under `wiki/papers/`, so a critic
that hallucinates a conclusion sentence out of thin air gets caught before
the verdict is built on fake evidence.

Usage (both defaults are cwd-relative -- run from the wiki instance root):
    python scripts/quote_check.py [--ledger wiki/novelty/ledger.md]
                                  [--papers wiki/papers]

Honest limitations (v0, by design): substring matching only -- it catches
fabrication (the quote exists in no paper note at all) but NOT
misattribution (张冠李戴): a real quote lifted from paper A but cited
against paper B still reports FOUND, because the search surface is *all*
of `wiki/papers/*.md`, not the single note the entry names. The reference
text is the *compiled* wiki note, not the raw/ original -- a quote
faithfully copied from an unfaithful compile passes; compile fidelity
against raw/ sources is a separate, later gate. Quote spans are scanned
line by line, so a quote wrapped across multiple ledger lines is not
paired (compiled ledgers keep each YAML evidence item on one line).

Quote extraction: spans inside 「」, “” (curly), or "" (ASCII) quotes.
ASCII spans on a `defense:` line are skipped -- the ledger schema defines
`defense` as `<一句话摘要>`, a summary, not a verbatim quote, and its YAML
scalar happens to be double-quoted, so scanning it would make every
well-formed entry MISS on its own defense field forever. A span counts as
a quote when its display form (zero-width characters removed, whitespace
runs folded to single spaces) is >= 10 characters; each quote is
attributed to the nearest preceding `## NC-...` case heading for
reporting, or "(preamble)" before the first case.

Matching normalization: both sides drop zero-width characters and *all*
whitespace, and paper text additionally drops line-leading markdown
blockquote markers (`>`). Fold-to-single-space is not enough for the
comparison itself: compiled notes hard-wrap CJK prose with no intended
space at the break, and quote blocks prefix every wrapped line with `> `,
so a genuinely verbatim quote would false-MISS under fold-to-space
comparison.

Exit codes: 0 = every quote found, 1 = one or more quotes missing,
2 = usage/IO error (ledger not found, or no paper notes to search).
Same convention as scripts/idea_lint.py.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

ZERO_WIDTH_RE = re.compile("[\u200b\u200c\u200d\u2060\ufeff]")
WHITESPACE_RUN_RE = re.compile(r"\s+")
BLOCKQUOTE_MARKER_RE = re.compile(r"^[ \t]*>+[ \t]?", re.MULTILINE)


def display_form(text: str) -> str:
    """Zero-width chars removed, whitespace runs folded to single spaces --
    the reporting form, and the form the >= 10 length threshold applies to."""
    return WHITESPACE_RUN_RE.sub(" ", ZERO_WIDTH_RE.sub("", text)).strip()


def match_key(text: str) -> str:
    """Zero-width chars and ALL whitespace removed -- the comparison form
    (see the module docstring's "Matching normalization" note)."""
    return WHITESPACE_RUN_RE.sub("", ZERO_WIDTH_RE.sub("", text))


# ---------------------------------------------------------------------------
# Ledger quote extraction
# ---------------------------------------------------------------------------

MIN_QUOTE_LEN = 10

CASE_HEADER_RE = re.compile(r"^##\s+(NC-\d+)")
DEFENSE_LINE_RE = re.compile(r"^\s*defense:")

CJK_QUOTE_RE = re.compile(r"「([^「」]+)」")
CURLY_QUOTE_RE = re.compile(r"“([^“”]+)”")
ASCII_QUOTE_RE = re.compile(r'"([^"]+)"')


@dataclass
class Quote:
    line: int  # 1-based ledger line the span sits on
    case: str  # nearest preceding NC- case number, or "(preamble)"
    display: str  # folded form, for reporting
    key: str  # whitespace-free form, for matching


def extract_quotes(ledger_text: str) -> list[Quote]:
    quotes: list[Quote] = []
    case = "(preamble)"
    for lineno, line in enumerate(ledger_text.splitlines(), start=1):
        header = CASE_HEADER_RE.match(line)
        if header:
            case = header.group(1)
            continue
        patterns = [CJK_QUOTE_RE, CURLY_QUOTE_RE]
        if not DEFENSE_LINE_RE.match(line):
            patterns.append(ASCII_QUOTE_RE)
        for pattern in patterns:
            for match in pattern.finditer(line):
                display = display_form(match.group(1))
                if len(display) < MIN_QUOTE_LEN:
                    continue
                quotes.append(Quote(lineno, case, display, match_key(match.group(1))))
    return quotes


# ---------------------------------------------------------------------------
# Paper search surface
# ---------------------------------------------------------------------------


def load_papers(papers_dir: Path) -> dict[str, str]:
    """Map each `*.md` under papers_dir (recursive, sorted) to its match key,
    with line-leading blockquote markers stripped before normalization."""
    surface: dict[str, str] = {}
    for path in sorted(papers_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        surface[path.name] = match_key(BLOCKQUOTE_MARKER_RE.sub("", text))
    return surface


def truncate(text: str, limit: int = 60) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="quote_check.py",
        description="Check that every ledger quote exists verbatim in wiki/papers/*.md.",
    )
    parser.add_argument(
        "--ledger",
        default="wiki/novelty/ledger.md",
        help="novelty ledger to scan for quotes (default: %(default)s)",
    )
    parser.add_argument(
        "--papers",
        default="wiki/papers",
        help="directory of compiled paper notes to search (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    ledger_path = Path(args.ledger)
    papers_dir = Path(args.papers)
    if not ledger_path.is_file():
        print(f"error: ledger not found: {ledger_path}", file=sys.stderr)
        sys.exit(2)
    if not papers_dir.is_dir():
        print(f"error: papers directory not found: {papers_dir}", file=sys.stderr)
        sys.exit(2)

    surface = load_papers(papers_dir)
    if not surface:
        print(f"error: no .md files found under {papers_dir}", file=sys.stderr)
        sys.exit(2)

    quotes = extract_quotes(ledger_path.read_text(encoding="utf-8"))

    missing = 0
    for quote in quotes:
        hits = [name for name, text in surface.items() if quote.key in text]
        if hits:
            print(
                f"{ledger_path}:{quote.line}: [FOUND] {quote.case} "
                f"<- {', '.join(hits)}: \"{truncate(quote.display)}\""
            )
        else:
            missing += 1
            print(f"{ledger_path}:{quote.line}: [MISS] {quote.case}: \"{truncate(quote.display)}\"")

    found = len(quotes) - missing
    print(
        f"{len(quotes)} quote(s) checked against {len(surface)} paper note(s): "
        f"{found} found, {missing} missing"
    )
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
