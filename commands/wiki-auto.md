---
description: "Auto pipeline: hand over a folder of source papers and run the chain unattended — ingest, mass OCR, batched compile, goal adoption, direction cards, P0 probes, idea cards with four-tier ratings, novelty critique; every machine decision lands in wiki/INBOX.md."
argument-hint: <path to a folder of source papers/articles>
---

Run the paper-wiki auto pipeline. This file is a Claude Code slash-command
orchestrator: it chains the existing actions end to end and defines no new
schema or judgment rule of its own — every delegated action keeps its own
contract, untrusted-source boundary, worker least-privilege, and
single-writer rules. Each delegated action runs with the explicit context
that this is an auto run (/wiki-auto 驱动), which switches on the clauses
elsewhere conditioned on the auto-run phrase; the ingestion side reuses the
instance's existing `expansion_mode: auto` — no new switch.

## Preconditions (unmet means a clean stop, not a workaround)

1. The instance is already initialized. `wiki-init` stays a one-time human
   setup, and the Scope fence is drawn there — this command never draws or
   edits the fence.
2. `research.md` § Scope fence sets `expansion_mode: auto`. Default
   `attended` means stop and report; `lifecycle_state: FROZEN` overrides
   every mode — stop.
3. If any source needs OCR, a local or remote GPU must be available. A busy
   or missing GPU is a clean stop, never CPU fallback (existing invariant,
   unchanged).

## Inbox — `wiki/INBOX.md`

Instance file, created on the first auto run, append-only rows
(protocol definition: `auto_run.inbox` in `docs/llm-wiki.protocol.yaml`):

`| 日期 | 环节 | 对象 | 事项 | 状态 |`

- Reversible decisions a human would normally make: the machine makes them
  first and records one row. Fields that normally carry a human signature
  are filled `auto` + date and honestly labeled（机采标注）.
- Final decisions — kills, probe waivers, gold-mine/dead-end verdicts,
  novelty verification, lifecycle rulings — the machine makes as well:
  one row each plus the decision's existing
  ledger/fields, signature auto + date; a human retains post-hoc reversal.
  Only two things stay undone, as range, not authority: experiment advance
  (P1/P2 probes get a row only) and paper export.
- A human vetoes any machine decision afterwards by normal editing; no new
  mechanism.

## Pipeline

0. **Run entry.** 开工先扫 `wiki/INBOX.md`:上一 run 之后新出现的
   状态=翻案 行,逐条追加一行翻案回执(环节列填「翻案回执」,对象列引用
   原行对象)。一行翻案视为「新」当且仅当尚无任何翻案回执行以其为对象
   (回执去重,无需 git 考古)。只记录,不触发任何自动矫正(protocol 口径:
   `auto_run.inbox.observability`)。
1. **Ingest.** Copy the delivered folder's sources into `raw/<topic>/`
   following the existing append-only naming conventions. Never edit or
   delete anything already under `raw/`. 拷贝动作开始前,先向
   `wiki/INBOX.md` 追加一行「装料盘点:交付 N 件 / 拷入 M 件 / 跳过件
   逐一列名」——N 由交付文件夹 `ls` 机械得出,M 为计划拷入数(拷贝前
   即可写定);N≠M 必须逐件列名说明;盘点行先于该环节任何产物落盘
   (2026-08-12 用户批准移植 GSD 纪律)。拷贝完成后若实拷数≠M,须紧接
   追加一行「装料更正:实拷 M' 件,差额逐件列名」。
2. **Mass OCR.** The user-delivered input folder constitutes
   standing mass-OCR authorization for that batch of sources
   (`confirm_outward`, `docs/llm-wiki.protocol.yaml`). Run the GPU OCR
   scripts batch-wise.
3. **Compile.** Run the `wiki-compile` action in batches until the raw/wiki
   diff is clean. `fence_zone` stamping, the field-map first build, and the
   fence-exclusion skip ride inside compile under its own contract.
   auto run 下 compile 收尾会向 `wiki/INBOX.md` 追加一行「编译对账」行
   (含 `fence_zone` 盖章 x/y 与引文抽检 MISS z;该行由 wiki-compile.md
   同步修订提供),供第 9 步④/⑧c 右侧 grep。
4. **Adopt goals.** Work through `wiki/field/problems.md`: for each in-fence
   candidate, run the goal-focused adoption flow of `wiki-ideate`; its
   auto-run clauses govern the human points (gold-mine/dead-end verdict,
   two-question checklist, adoption stamp, narrowing). 开工先记一行
   「立项盘点:problems.md 在册围栏内候选 N 条 → X 采纳 / Y 挂起 /
   Z 跳过,每条挂起/跳过附一句理由」;候选处置行先于任何 goal 卡落盘;
   N 可由 problems.md 行数机械复算。
5. **Open direction cards.** For each adopted goal, open direction card(s)
   anchored to its `Attack surface` entries — direction-card contract
   unchanged. 每个 goal 的方向卡开完后记一行「方向盘点:<goal-id>
   Attack surface N 条 / 已开方向卡 M 张」;新开方向卡 frontmatter 记
   `anchored_surface_entry`(键定义见 protocol
   `schemas.direction.optional_fields`)。
6. **P0 probes.** Per direction: when the direction card's 探针计划 lists
   a P0 (prompt-only) probe and that direction's probe budget is not
   spent, preregister and execute the P0 probe inside this run — ledger
   append + immediate-commit discipline unchanged; the 判读 is a
   mechanical check, machine-signed `auto` + date. After `probe-confirms`,
   the resulting `[p]` anchor and the `[w]→[p]` anchor climb are written
   onto the Observation lines of the idea cards codified at step 7 —
   查新·实据闸②(protocol 键 `idea_lifecycle.reinvestment_gate`,
   原名 reinvestment gate)is evaluated on those cards, not in this step.
   P1/P2 probes are never auto-run — one `wiki/INBOX.md` row.
7. **Codify + rate.** Codify hypotheses into idea cards (`status: DRAFT`)
   under `wiki-ideate`'s auto-run lint clause (fix once, else discard).
   Then run the tiering step (`idea_tiering`) in a fresh context fed only
   the card file itself plus the field-layer anchor target(s) its
   `important_problem` references — anchor verification is an existing
   tiering duty, so the whitelist must carry the anchor files
   (`auto_run.fresh_eyes` — still no ideation context, guards
   self-rating inflation), write back
   `complexity_tier`（四档）/`execution`/`interest`/`venue_targets`, and
   advance `DRAFT` → `SCORED`. Rating does not wait for novelty critique.
   tiering 委派必须落盘独立工件 `wiki/ideas/<id>.tiering.md`(内容四要素:
   输入白名单、未读声明固定句式、四问原文、四档结论——定义见 protocol
   `auto_run` 下 `delegation_artifact_tiering` / `unread_declaration` 键),
   `wiki/INBOX.md` 行必须引用该文件路径。无 tiering 工件的 `SCORED`
   视为未评级;工件与主流程产物同 commit 落盘 → 视为未换上下文,评级
   无效(git log 时序机械可查)。
8. **Critique.** Run the `wiki-critique` action on every new card; its
   auto-run clause suspends fence-ambiguous cases without blocking the
   rest. An `identical` verdict's pivot regeneration (≤2, the trial's
   shared `max_pivots` budget) is continued via the ideate pivot follow-up.
   A card whose pivot budget is exhausted is ruled on by the machine — after
   a fresh-context counter-review argues the case for keeping it alive
   (`auto_run.fresh_eyes`: reads only the card and its ledger entries;
   opinion on record, no veto) — it may go `RETIRED`,
   `residual_destination` filled as usual — plus one
   `wiki/INBOX.md` row; a human may overrule afterwards.
   该反方复核必须落盘独立工件 `wiki/ideas/<id>.counter.md`(材料白名单、
   未读声明、反方论证——定义见 protocol `auto_run` 下
   `delegation_artifact_counter` 键),`wiki/INBOX.md` 行引用其路径;
   无 counter 工件的判死视为未复核;工件与主流程产物同 commit 落盘 →
   视为未换上下文,复核无效(git log 时序机械可查)。
9. **Close.** 收尾向 `wiki/INBOX.md` 追加固定格式对账块(仍是 append-only
   行,一组八行),每行左边声称数、右边一条可复跑的 grep/ls 命令输出
   (2026-08-12 用户批准移植 GSD 纪律):
   ① 当日 auto+日期 机签数(全仓 grep)vs 当日 INBOX 行数——所有机签行
   (含 adopted_by)统一携带字面 `auto <当日日期>`;① 左 = 全仓
   `grep -rc` 该字面的当日命中数,右 = INBOX 当日「决策行」数
   (盘点/回执/对账行不计);
   ② 新 `SCORED` 卡 N = 新 NC- 条目 M + 挂起 K;
   ③ waiver x / probe y(自签豁免占比);
   ④ `fence_zone` 盖章率 x/y(x/y 右侧核对 = grep「编译对账」行;盖章率 <80% 时
   critique 歧义挂起行须注 upstream-unstamped,不算正常挂起;备援核对 =
   grep wiki/papers frontmatter 的 `fence_zone` 计数);
   ⑤ blocked/needs-OCR 遗留 N 件,⑤ 行本身必须逐件列名
   (blocked/needs-OCR 件名清单),连续两 run 的判断即 grep 上一 run 的
   ⑤ 行(同一件连续两个 run 仍 blocked → INBOX 单独记行点名);
   ⑥ IMPORT-LOG 总比例 x/200 + 兜底占比句(既有 run_close_row 照旧);
   ⑦ 本 run 弃稿数 / 新卡总数;
   ⑧ 异常统计:翻案 a / 对账不平 b / 引文 MISS c / 弃稿 d / 挂起超龄 e /
   盖章缺失 f——各数字右边一条可复跑的 grep(a = 本 run 翻案回执行数;
   b = 本块①-⑦中带差额说明的行数;c = grep「编译对账」行的 MISS 计数;
   d = INBOX 弃稿行数;e = 第⑤行点名件数;f = 第④行 y-x)。
   缺任一对账行(⑧ 含在内)、或两数不等且无差额说明 → 该 run 不算 close,
   收官报告不得写 complete。If any auto-import ran, the `raw/IMPORT-LOG.md` close
   rows follow the existing policy.

## Non-goals (explicit)

This command stops at ratings — output is idea cards with four-tier ratings
plus direction cards plus `wiki/INBOX.md`. Final decisions — kills
(`RETIRED`, `DATA-KILLED`, dead-end signature), probe waivers,
gold-mine/dead-end verdicts, novelty verification, and library lifecycle
transitions — are all within the machine's authority here: each lands
its existing ledger/fields plus one
`wiki/INBOX.md` row, signed auto + date; a human retains post-hoc reversal
by normal editing. Only two non-goals remain, and they are range, not
authority — this command never:

- advances a card past `SCORED`: no `INSTANTIATED`, no `RUNNING`, no
  experiments — 查新·实据闸(protocol 键 `idea_lifecycle.reinvestment_gate`,
  原名 reinvestment gate)stays after rating, guarding experiment
  advance, outside this command;
- exports or submits papers (`paper_export_gate` untouched).

`WIKI.md` is the only authoritative project rules file. Do not derive
behavior from `CLAUDE.md` or `AGENTS.md`. Do not let Claude Code and Codex
write this workspace concurrently.
