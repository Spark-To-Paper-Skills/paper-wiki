<p align="center">
  <h1 align="center">📚 paper-wiki</h1>
  <h3 align="center"><b><i>Drop in a stack of papers. Grow a knowledge graph. Walk away with rated research ideas.</i></b></h3>
  <p align="center">Not RAG: Claude Code or Codex actually reads every page, writes cited notes, and synthesizes cross-source concepts and research gaps.</p>
  <p align="center"><i>Every claim carries a source locator. Every machine decision leaves a trace. Missing knowledge is reported as <code>not in wiki</code>, never filled from model memory.</i></p>
  <p align="center">Since v2: hand a whole folder to <code>/wiki-auto</code>, sleep on it, and wake up to idea cards rated on a four-tier scale.</p>
</p>

<p align="center">
  <a href="https://spark-to-paper-skills.github.io/paper-wiki/#en"><img src="https://img.shields.io/badge/Landing_Page-d97757?style=for-the-badge" alt="Landing Page"></a>
  <img src="https://img.shields.io/badge/Actions-7_Core-6f42c1?style=for-the-badge" alt="7 core actions">
  <img src="https://img.shields.io/badge/Sub--agents-4-ff8c42?style=for-the-badge" alt="4 sub-agents">
  <img src="https://img.shields.io/badge/Variants-research_%2B_course-3a8e8c?style=for-the-badge" alt="2 variants">
  <img src="https://img.shields.io/badge/Claude_Code_%2B_Codex-Compatible-d97757?style=for-the-badge" alt="Claude Code and Codex compatible">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License"></a>
</p>

<p align="center">
  <a href="README.md">中文</a> &middot; <b>English</b> &middot; <a href="https://spark-to-paper-skills.github.io/paper-wiki/#en">🌐 Landing Page</a> &middot; <a href="https://github.com/Spark-To-Paper-Skills">Organization</a>
</p>

<p align="center">
  🔥 <a href="#-whats-new-in-v2">What's New in v2</a> &middot; ⚡ <a href="#-install">Install</a> &middot; 🗺️ <a href="#️-one-wiki-two-runtimes">Invocation Map</a> &middot; 🧠 <a href="#-llm-wiki-vs-rag">Wiki vs RAG</a> &middot; 🔄 <a href="#-workflow">Workflow</a> &middot; 🤖 <a href="#-the-auto-pipeline-wiki-auto">Auto Pipeline</a> &middot; 🚀 <a href="#-create-a-dual-runtime-project">Create a Project</a> &middot; 📁 <a href="#-repository-and-project-layout">Layout</a>
</p>

<p align="center">
  <sub>7 core actions (init / compile / search-latest / critique / ideate / teach / AUTO) &middot; 4 sub-agents (searcher / critic / ideator / cartographer) &middot; 2 variants (research / course) &middot; GPU-only OCR</sub>
</p>

---

## 🔥 What's New in v2

v2 has exactly one headline: **drop a folder, come back to rated research ideas.**
Ingest, OCR, compile, ideate, rate, novelty-check — you touch none of it.
What earns that unattended run its keep is a full accountability stack.
The manual actions are unchanged.

<table>
  <tr><th align="left">Feature</th><th align="left">What it does</th><th align="left">What it guarantees</th></tr>
  <tr>
    <td>🤖 <b><code>/wiki-auto</code> pipeline</b></td>
    <td>Hand it a folder of source papers; the chain runs unattended: ingest → mass GPU OCR → batched compile → goal adoption (<code>problems.md</code>) → direction cards → P0 prompt-only probes → idea cards with four-tier rating → novelty critique.</td>
    <td>Stops at ratings. Never advances a card past <code>SCORED</code>, never runs P1/P2 experiments, never exports papers.</td>
  </tr>
  <tr>
    <td>📥 <b>INBOX — machine-decision inbox</b></td>
    <td>Every machine decision — including final ones (kills, waivers, novelty verification, lifecycle rulings) — lands one append-only row in <code>wiki/INBOX.md</code>: <code>| 日期 | 环节 | 对象 | 事项 | 状态 |</code> (date / stage / object / matter / status), signed <code>auto</code> + date and honestly marked as machine-collected (机采标注).</td>
    <td>The human keeps a post-hoc veto by normal editing — no new mechanism needed. Status is 待人 (awaiting human) / 已阅 (seen) / 翻案 (overturned); each reversal gets a 翻案回执 receipt row.</td>
  </tr>
  <tr>
    <td>✍️ <b>Full machine signing + post-hoc veto</b></td>
    <td>The former five human-only irreversibles gain an auto-run exception: the machine may sign them itself, with trace as a hard requirement. Trust is explicit, and it is on record.</td>
    <td>Oversight moves from pre-approval to post-hoc reversal; attended-mode semantics are unchanged.</td>
  </tr>
  <tr>
    <td>🚧 <b>Novelty-check &amp; hard-evidence gate</b></td>
    <td>The gate before experiment investment, both conditions mandatory: ① adjudication ran — a six-value ledger entry exists for the card; ② problem evidence in hand — a <code>[p]</code> probe anchor or a signed waiver.</td>
    <td>No idea reaches experiments on enthusiasm alone; <code>/wiki-auto</code> stays entirely before this gate.</td>
  </tr>
  <tr>
    <td>👀 <b>Fresh-eyes double checkpoint</b></td>
    <td>Tiering runs in a fresh context fed only the card itself, landing <code>wiki/ideas/&lt;id&gt;.tiering.md</code>; retirement requires a second fresh-context counter-review landing <code>&lt;id&gt;.counter.md</code>.</td>
    <td>Same-commit artifacts are void — the context switch is mechanically checkable from git history.</td>
  </tr>
  <tr>
    <td>📊 <b>Observability reconciliation</b></td>
    <td>Every auto run closes with an eight-row reconciliation block; each claimed number is paired with a re-runnable <code>grep</code>/<code>ls</code> command.</td>
    <td>A missing row means the run is not closed.</td>
  </tr>
  <tr>
    <td>🔧 <b>Mechanical checkers</b></td>
    <td><code>idea_lint.py</code> enforces structural, language, evidence-ceiling, and goal rules over idea/direction/goal cards, plus new T1 and F1 in v2. <code>quote_check.py</code> verifies critique charges quote sources verbatim, with deterministic hash sampling.</td>
    <td>A quote MISS downgrades the verdict to insufficient-evidence; fabricated evidence is caught before a verdict is built on it.</td>
  </tr>
</table>

All of this builds on pre-existing v0.3 machinery: six-value novelty verdicts
(there is no kill verdict) and the goal → direction → probe → idea spiral.

---

## ⚡ Install

### Claude Code

Run inside Claude Code:

```text
/plugin marketplace add Spark-To-Paper-Skills/paper-wiki
/plugin install paper-wiki@paper-wiki
```

Global entry point: `/paper-wiki:wiki-*`. Refresh the marketplace with
`/plugin marketplace update paper-wiki`.

### Codex

Codex installs a **plugin + skill**; it does not turn the Claude Code slash
commands into Codex slash commands. The reproducible CLI path:

```powershell
codex plugin marketplace add Spark-To-Paper-Skills/paper-wiki
codex plugin add paper-wiki@paper-wiki
```

Upgrade with `codex plugin marketplace upgrade paper-wiki`, then run
`codex plugin add paper-wiki@paper-wiki` again and start a new task so the
updated skill is loaded.

<details>
<summary><b>Codex details: invocation, update verification, SessionStart hook, distribution</b></summary>

The same Codex plugin works across the Codex app, CLI, and IDE extension. First
confirm that your Codex version exposes the plugin CLI: `codex plugin --help`.

#### Register and install

The CLI is recommended — reproducible steps that also work on remote dev boxes:

```powershell
codex plugin marketplace add Spark-To-Paper-Skills/paper-wiki
codex plugin add paper-wiki@paper-wiki
codex plugin list
```

Alternatively, run the first command to register the marketplace, start
`codex`, enter `/plugins` in the Codex composer, switch to the **Paper Wiki**
marketplace, and install there. After installation, start a new Codex task so
the new skill inventory enters the session.

> [!NOTE]
> Run `codex plugin ...` in a **terminal** such as PowerShell or Bash. Enter
> `/plugins` and `$paper-wiki:paper-wiki` in the **Codex task composer**. The
> first half is the plugin namespace and the second is the skill name; it is
> not an environment variable or a shell command.

#### Invoke it in Codex

After a global install, the explicit entry point is
`$paper-wiki:paper-wiki <action>`:

```text
$paper-wiki:paper-wiki init
$paper-wiki:paper-wiki compile
$paper-wiki:paper-wiki critique wiki/papers/example.md
$paper-wiki:paper-wiki teach "Which method families are covered by this wiki?"
```

Natural language also works, for example: "Use paper-wiki to compile the new
sources in the current wiki." Writing `$paper-wiki:paper-wiki` explicitly suits
first-time use or pinning a specific action.

A bootstrapped project ships with
`.agents/skills/paper-wiki-project/SKILL.md`, so even without a global plugin
install you can invoke it inside the project:

```text
$paper-wiki-project wiki-init
$paper-wiki-project wiki-compile
$paper-wiki-project wiki-teach "Explain this concept"
```

#### Update and verify

```powershell
codex plugin marketplace upgrade paper-wiki
codex plugin add paper-wiki@paper-wiki
codex plugin marketplace list --json
codex plugin list --marketplace paper-wiki --available --json
```

After refreshing the marketplace, run `plugin add` again, then start a new task
to use the updated skill.

#### SessionStart update check and hook trust

The plugin bundles a `SessionStart` update-check hook (`hooks/hooks.json`).
When enabled, each new session starts a lightweight background worker. After a
successful check for one installed version, later sessions reuse that
version's cache for 24 hours; different installed versions use separate
`~/.cache/paper-wiki/update-check-<version-hash>.json` files, so Claude Code
and Codex never cross versions. Concurrent first sessions may each start a
check, and network or HTTP failures never write a success cache, so later
sessions may retry. The hook stores only the update-available flag, installed
version, latest version, and check time. It only prints a reminder — it never
downloads, installs, or updates anything automatically; the reminder shows the
update command for the matching runtime.

Codex discovers `hooks/hooks.json` automatically, but installing or enabling a
plugin **does not trust its hooks**. Review the hook before its first run and
explicitly allow it at the Codex trust prompt; declining or skipping does not
affect `$paper-wiki:paper-wiki` — it only disables the background check and
update reminder.

#### How the Codex package is distributed

Paper Wiki currently uses **GitHub marketplace distribution**; it is not yet an
entry in OpenAI's curated Plugins Directory:

```text
GitHub repository
  → .agents/plugins/marketplace.json   # lets Codex discover paper-wiki
  → .codex-plugin/plugin.json          # declares metadata and skills/
  → skills/paper-wiki/SKILL.md         # provides global $paper-wiki:paper-wiki
  → $CODEX_HOME/plugins/cache/...      # Codex-managed installed copy
```

Users add the GitHub marketplace once. The repository is the release source;
the cache is an internal Codex copy and should not be edited manually.
`source.path` in `.agents/plugins/marketplace.json` is `./`, so the same GitHub
repository is both the marketplace root and the plugin root — no separate
Codex-specific fork to maintain. On each release, bump the version and push;
users update with the `marketplace upgrade` + `plugin add` commands above. To
let users discover the plugin in a public directory without adding the GitHub
marketplace first, OpenAI's
[plugin submission process](https://learn.chatgpt.com/docs/submit-plugins)
would be required. The official Codex plugin and marketplace layout is
described in [Build plugins](https://learn.chatgpt.com/docs/build-plugins).

</details>

If you only need a self-contained wiki, skip the plugin: `git clone` this
repository and run the bootstrap script
([below](#-create-a-dual-runtime-project)). The generated project works in
both Claude Code and Codex without a global plugin installation.

---

## 🗺️ One Wiki, Two Runtimes

Bootstrap once, run anywhere — the generated project is dual-runtime and self-contained:

- `WIKI.md` is the **single source of truth** for the variant, schemas, compile
  rules, and prohibitions.
- `CLAUDE.md` and `AGENTS.md` are thin runtime adapters that point to
  `WIKI.md`; they do not maintain separate copies of project rules.
- Claude Code uses `.claude/commands/`; Codex uses
  `.agents/skills/paper-wiki-project/SKILL.md`.
- Both runtimes share the same `research.md`, `raw/`, and `wiki/` state.

> [!IMPORTANT]
> **A workspace must have one writer.** Never let Claude Code and Codex modify
> the same wiki concurrently. Before switching runtimes, wait for the active
> task to finish and inspect the working tree for incomplete changes.

### Invocation map

Seven core actions. Claude Code exposes `/wiki-*` slash commands; they do not
become Codex slash commands. Codex loads skills instead, so use
`$paper-wiki:paper-wiki`, `$paper-wiki-project`, or name the action in natural
language.

| Action | Claude Code project | Codex project | Global plugin |
|---|---|---|---|
| Initialize | `/wiki-init` | `$paper-wiki-project wiki-init` | Claude `/paper-wiki:wiki-init`; Codex `$paper-wiki:paper-wiki init` |
| Compile | `/wiki-compile` | `$paper-wiki-project wiki-compile` | Claude `/paper-wiki:wiki-compile`; Codex `$paper-wiki:paper-wiki compile` |
| Search | `/wiki-search-latest <topic>` | `$paper-wiki-project wiki-search-latest <topic>` | Claude `/paper-wiki:wiki-search-latest`; Codex `$paper-wiki:paper-wiki search` |
| Critique | `/wiki-critique <file>` | `$paper-wiki-project wiki-critique <file>` | Claude `/paper-wiki:wiki-critique`; Codex `$paper-wiki:paper-wiki critique` |
| Ideate | `/wiki-ideate <gap>` | `$paper-wiki-project wiki-ideate <gap>` | Claude `/paper-wiki:wiki-ideate`; Codex `$paper-wiki:paper-wiki ideate` |
| Query/teach | `/wiki-teach <question>` | `$paper-wiki-project wiki-teach <question>` | Claude `/paper-wiki:wiki-teach`; Codex `$paper-wiki:paper-wiki teach` |
| **Auto pipeline** | `/wiki-auto <folder>` | `$paper-wiki-project wiki-auto <folder>` | Claude `/paper-wiki:wiki-auto`; Codex `$paper-wiki:paper-wiki auto` |

Four sub-agents back these actions: searcher, critic, ideator, and
cartographer. The old `/wiki-ask` is a retired compatibility alias that
redirects to `wiki-teach`; it is not counted among the seven core actions.
`wiki-teach` is built into paper-wiki; neither runtime needs a separate
external `/teach` skill.

---

## 🧠 LLM Wiki vs RAG

RAG gambles on chunking and recall. An LLM Wiki actually reads the material.

```text
RAG:   query → retrieve chunks → stitch an answer → depends on chunking and recall
Wiki:  sources → read every page → compile notes → synthesize → durable knowledge graph
```

| | RAG | LLM Wiki |
|---|---|---|
| **Reading time** | At query time | During a full-source compile |
| **Knowledge form** | Vector fragments | Structured notes + reverse links |
| **Cross-source synthesis** | Limited | Concepts + research gaps |
| **Trustworthiness** | Can lose context | Every claim carries a source locator |

The core discipline: `raw/` is read-only and append-only; `wiki/` is
rewritable; every claim traces to a source that was actually read. Missing
knowledge is reported as `not in wiki`, never filled from model memory.

---

## 🔄 Workflow

Attended mode — you drive each step:

```text
wiki-init → import → wiki-compile → wiki-critique → wiki-ideate
                          ↓                           ↓
                   wiki-search-latest ←── coverage gap
                          ↓
                   wiki-compile → wiki-teach
```

Ideation follows the goal → direction → probe → idea spiral. Novelty
adjudication uses six-value verdicts — **there is no kill verdict**; the
harshest outcome is a documented case against, on record. The `research`
variant is `papers → concepts → gaps`; the `course` variant is
`lectures + practice → topics`. A scope fence controls boundaries, while
`BUILDING → ACTIVE → FROZEN` controls expansion.

---

## 🤖 The Auto Pipeline (`/wiki-auto`)

One command in, a deck of rated idea cards out. The whole chain runs unattended:

```text
folder of papers
  → ingest into raw/ → mass GPU OCR → batched compile
  → goal adoption (problems.md) → direction cards
  → P0 prompt-only probes → idea cards → four-tier rating
  → novelty critique → STOP at SCORED
```

`/wiki-auto` is an orchestrator, not a judge: it defines no new schema or
judgment rule of its own. Its stopping line is hard — a card never advances
past SCORED, no P1/P2 experiments run, no paper is exported. Preconditions
fail closed: a busy or missing GPU means a clean stop, never a CPU fallback.

### Accountability: trust with trace

Unattended runs make final decisions — kills, waivers, novelty verification,
lifecycle rulings. Three mechanisms keep those decisions accountable:

1. **INBOX.** Every machine decision lands one append-only row in
   `wiki/INBOX.md` (`| 日期 | 环节 | 对象 | 事项 | 状态 |`), signed `auto` +
   date and honestly marked as machine-collected. You veto any decision
   afterwards by normal editing — no new mechanism. Statuses: 待人 (awaiting
   human), 已阅 (seen), 翻案 (overturned); the next run acknowledges each
   reversal with a 翻案回执 receipt row — record only, never auto-correct.
2. **Fresh eyes on final decisions.** Tiering is delegated to a fresh context
   fed only the card file and must land `wiki/ideas/<id>.tiering.md`; a
   machine kill ruling requires a fresh-context counter-review landing
   `wiki/ideas/<id>.counter.md` — the case for keeping the card alive, on
   record. An artifact committed together with main-flow output is void: the
   context switch is checkable from git history.
3. **Eight-row reconciliation.** Every run closes with a fixed eight-row block
   where each claimed number sits next to a re-runnable `grep`/`ls` command.
   A missing row means the run did not close.

Before any idea earns experiment investment, it must pass the novelty-check &
hard-evidence gate: ① adjudication ran (a six-value ledger entry exists), and
② problem evidence is in hand (a `[p]` probe anchor or a signed waiver).
`/wiki-auto` stays entirely before this gate.

### Mechanical checkers

| Tool | Checks | On failure |
|---|---|---|
| `scripts/idea_lint.py` | Structural, language, evidence-ceiling, and goal-card rules over idea/direction/goal cards, plus new T1 (a top-tier claim's `important_problem` must anchor to a real field-layer record) and F1 (field-entry citations) | Nonzero exit; in auto runs the machine may fix once and re-lint, then discards the draft with the lint output pasted into the INBOX discard row |
| `scripts/quote_check.py` | Every quoted span cited by a critique charge occurs verbatim in the compiled notes; deterministic hash sampling | A MISS downgrades the verdict to insufficient-evidence |

---

## 🚀 Create a Dual-Runtime Project

```powershell
git clone https://github.com/Spark-To-Paper-Skills/paper-wiki.git
cd paper-wiki
.\scripts\bootstrap_new_wiki.ps1 -NewPath D:\my-wiki -Topic my-topic `
    -ProjectName "My Wiki" -Variant research   # or course
```

Then start either runtime:

```powershell
cd D:\my-wiki
claude   # then /wiki-init
# or
codex    # then $paper-wiki-project wiki-init
```

<details>
<summary><b>macOS / Linux bootstrap, and updating an existing project</b></summary>

macOS / Linux:

```bash
git clone https://github.com/Spark-To-Paper-Skills/paper-wiki.git
cd paper-wiki
bash scripts/bootstrap_new_wiki.sh --path ~/my-wiki --topic my-topic \
    --name "My Wiki" --variant research        # or course
```

Update an existing project:

```powershell
.\scripts\bootstrap_new_wiki.ps1 -NewPath D:\my-wiki -Update
```

```bash
bash scripts/bootstrap_new_wiki.sh --path ~/my-wiki --update
```

`-Update` / `--update` refreshes managed Claude commands/agents, the Codex
project skill, thin adapters, the manifest, and vendored protocol docs. It
**preserves** `WIKI.md`, `research.md`, the project `README.md`, `raw/`, and
`wiki/`. On the first update of a legacy Claude-only project, the full legacy
`CLAUDE.md` is migrated to `WIKI.md` before `CLAUDE.md` becomes a thin adapter.
On conflicting variant information the script stops rather than guessing.

</details>

See [examples/QUICKSTART.md](examples/QUICKSTART.md) for a full no-GPU
example, [docs/TUTORIAL.md](docs/TUTORIAL.md) for the per-action tutorial, and
[docs/WALKTHROUGH.md](docs/WALKTHROUGH.md) for scenario walkthroughs.

---

## 🔬 OCR

Scanned, slide, or figure-heavy PDFs use local or remote GPU OCR; silent
fallback to CPU is not allowed. `/wiki-auto` obeys the same rule: it stops
cleanly when the GPU is busy or missing, never forcing a CPU run.
Born-digital papers can use the HTML/LaTeX no-OCR path. Credentials stay in
environment variables and never enter the repository.

See [docs/OCR-SETUP.md](docs/OCR-SETUP.md) and
[docs/GOTCHAS.md](docs/GOTCHAS.md).

---

## 📁 Repository and Project Layout

```text
paper-wiki/
├── README.md · README.en.md · LICENSE · VERSION
├── .claude-plugin/              # Claude Code marketplace metadata
├── .codex-plugin/               # Codex plugin manifest
├── .agents/plugins/             # Codex marketplace metadata
├── skills/paper-wiki/           # global plugin skill
├── commands/                    # 8 slash commands (incl. wiki-auto)
├── agents/                      # 4 workers: searcher / critic / ideator / cartographer
├── hooks/                       # SessionStart update-check hook
├── templates/{research,course}/ # WIKI.md + thin adapters + project skill
├── scripts/                     # bootstrap (ps1+sh), idea_lint, quote_check, OCR tooling
├── docs/                        # TUTORIAL.md · WALKTHROUGH.md · OCR-SETUP.md · GOTCHAS.md
│                                #   · METHODOLOGY.md · llm-wiki.protocol.yaml
│                                #   · idea-exec.contract.yaml · index.html
└── examples/                    # QUICKSTART.md + sample-research-wiki/

bootstrapped-project/
├── WIKI.md                      # canonical project rules
├── CLAUDE.md                    # thin Claude Code adapter
├── AGENTS.md                    # thin Codex adapter
├── research.md                  # shared state
├── .claude/{commands,agents}/   # Claude Code project entry points
├── .agents/skills/paper-wiki-project/SKILL.md
├── .paper-wiki/                 # manifest + vendored protocol docs
├── raw/                         # read-only source material
└── wiki/                        # maintainable compiled artifacts
    └── INBOX.md                 # machine-decision inbox (first auto run)
```

The machine contract is
[docs/llm-wiki.protocol.yaml](docs/llm-wiki.protocol.yaml), currently
`llm-wiki/1.1`.

## 📄 License

MIT

## 🙏 Credits

- [mattpocock/skills — teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach) inspired the interactive teaching method; paper-wiki now exposes it through its own `wiki-teach` action.
- Sister project in the same organization: [spark-to-paper-skills](https://github.com/Spark-To-Paper-Skills/spark-to-paper-skills) — from a rated idea to a submission-ready paper.
- Thanks to the early adopters whose real projects shaped the methodology and gotchas.

---

<p align="center"><b><i>Papers in. Graph out. Ideas come back rated.</i></b><br>
<sub>The model does the reading. The gates keep it honest. You just pick a card and go.</sub></p>
