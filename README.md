<p align="center">
  <h1 align="center">📚 paper-wiki</h1>
  <h3 align="center"><b><i>丢进一摞论文。长出一张知识图谱。拿走带评级的研究 idea。</i></b></h3>
  <p align="center">不是 RAG：Claude Code 或 Codex 把每一页真读完，写成带引用的笔记，再综合出跨源概念与研究空白。</p>
  <p align="center"><i>每条主张有出处。每个机器决策有留痕。wiki 没有的内容明说 <code>not in wiki</code>，绝不拿模型记忆补齐。</i></p>
  <p align="center">v2 起，把整个文件夹交给 <code>/wiki-auto</code>：睡一觉，醒来收获带四档评级的 idea 卡。</p>
</p>

<p align="center">
  <a href="https://spark-to-paper-skills.github.io/paper-wiki/"><img src="https://img.shields.io/badge/Landing_Page-d97757?style=for-the-badge" alt="Landing Page"></a>
  <img src="https://img.shields.io/badge/Actions-7_Core-6f42c1?style=for-the-badge" alt="7 core actions">
  <img src="https://img.shields.io/badge/Sub--agents-4-ff8c42?style=for-the-badge" alt="4 sub-agents">
  <img src="https://img.shields.io/badge/Variants-research_%2B_course-3a8e8c?style=for-the-badge" alt="2 variants">
  <img src="https://img.shields.io/badge/Claude_Code_%2B_Codex-Compatible-d97757?style=for-the-badge" alt="Claude Code and Codex compatible">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License"></a>
</p>

<p align="center">
  <a href="README.en.md">English</a> &middot; <b>中文</b> &middot; <a href="https://spark-to-paper-skills.github.io/paper-wiki/">🌐 项目主页</a> &middot; <a href="https://github.com/Spark-To-Paper-Skills">组织主页</a>
</p>

<p align="center">
  🔥 <a href="#-v2-新特性">v2 新特性</a> &middot; ⚡ <a href="#-安装">安装</a> &middot; 🗺️ <a href="#️-一套-wiki两端操作">调用映射</a> &middot; 🧠 <a href="#-llm-wiki-vs-rag">Wiki vs RAG</a> &middot; 🔄 <a href="#-工作流">工作流</a> &middot; 🤖 <a href="#-自动流水线wiki-auto">自动流水线</a> &middot; 🚀 <a href="#-创建双端项目">创建项目</a> &middot; 📁 <a href="#-仓库与生成项目结构">结构</a>
</p>

<p align="center">
  <sub>7 核心 action（init / compile / search-latest / critique / ideate / teach / AUTO）&middot; 4 sub-agent（searcher / critic / ideator / cartographer）&middot; 2 变体（research / course）&middot; GPU-only OCR</sub>
</p>

---

## 🔥 v2 新特性

v2 的头条只有一个：**丢进一个文件夹，醒来收获带四档评级的 idea 卡。**
入库、OCR、编译、构思、评级、查新——中间每一步都不用你碰。
撑起这份底气的，是一整套让「无人值守」站得住的追责机制。手动 action 的语义一律不变。

<table>
  <tr><th align="left">特性</th><th align="left">做什么</th><th align="left">保证什么</th></tr>
  <tr>
    <td>🤖 <b><code>/wiki-auto</code> 自动流水线</b></td>
    <td>把装满源论文的文件夹交给它，链条无人值守跑完：入库 → 批量 GPU OCR → 分批编译 → 目标认领（<code>problems.md</code>）→ 方向卡 → P0 纯 prompt 探针 → 四档评级的 idea 卡 → 查新审查。</td>
    <td>止于评级。绝不把卡片推过 <code>SCORED</code>，绝不跑 P1/P2 实验，绝不导出论文。</td>
  </tr>
  <tr>
    <td>📥 <b>INBOX 机器决策收件箱</b></td>
    <td>每个机器决策——包括终局决策（判死、豁免、查新核验、生命周期裁定）——都在 <code>wiki/INBOX.md</code> 这张只追加的表里落一行：<code>| 日期 | 环节 | 对象 | 事项 | 状态 |</code>，署名 <code>auto</code> + 日期，诚实标注「机采标注」。</td>
    <td>人用普通编辑就保留事后否决，不需要新机制。状态取 待人 / 已阅 / 翻案；每次翻案配一条翻案回执。</td>
  </tr>
  <tr>
    <td>✍️ <b>全量机签 + 事后否决</b></td>
    <td>原先五类只许人签的不可逆决定，auto 运行下开例外：机器可以自签，但留痕是硬要求。信任显式给出，白纸黑字记录在案。</td>
    <td>监督从事前审批移到事后翻案；值守模式的语义不变。</td>
  </tr>
  <tr>
    <td>🚧 <b>查新·实据闸</b></td>
    <td>实验投入前的闸门，两个条件缺一不可：① 查新裁决跑过——六值台账里有这张卡的记录；② 问题实据在手——卡片带 <code>[p]</code> 探针锚点，或有签字豁免。</td>
    <td>没有 idea 只凭热情进实验；<code>/wiki-auto</code> 整条停在闸前。</td>
  </tr>
  <tr>
    <td>👀 <b>Fresh-eyes 双检查点</b></td>
    <td>评级在只喂卡片本身的全新上下文里做，落成 <code>wiki/ideas/&lt;id&gt;.tiering.md</code>；判退休要再开一个全新上下文做反方复核，落成 <code>&lt;id&gt;.counter.md</code>。</td>
    <td>与主流程同一 commit 提交的工件视为无效——上下文切换可由 git 时序机械核查。</td>
  </tr>
  <tr>
    <td>📊 <b>可观测性对账</b></td>
    <td>每次 auto 运行收尾必出八行对账块，每个报出来的数字旁边配一条可重跑的 <code>grep</code>/<code>ls</code> 命令。</td>
    <td>缺一行，这次运行就不算收尾。</td>
  </tr>
  <tr>
    <td>🔧 <b>机械核查工具</b></td>
    <td><code>idea_lint.py</code>：对 idea/方向/目标卡做结构、语言、证据上限、目标规则检查，另加 v2 新增的 T1、F1 两条。<code>quote_check.py</code>：对审查指控做逐字引文核验，确定性哈希抽样。</td>
    <td>引文 MISS 会把结论降级为证据不足；捏造的证据在裁定建立之前就被抓住。</td>
  </tr>
</table>

这套机制建立在 v0.3 既有机制之上：六值查新结论（没有「判死」这一档）、
goal → direction → probe → idea 螺旋。

---

## ⚡ 安装

### Claude Code

在 Claude Code 中运行：

```text
/plugin marketplace add Spark-To-Paper-Skills/paper-wiki
/plugin install paper-wiki@paper-wiki
```

全局入口是 `/paper-wiki:wiki-*`。更新 marketplace：
`/plugin marketplace update paper-wiki`。

### Codex

Codex 端安装的是 **plugin + skill**，不是把 Claude Code 的 slash commands
原样搬过去。可复现的 CLI 路径：

```powershell
codex plugin marketplace add Spark-To-Paper-Skills/paper-wiki
codex plugin add paper-wiki@paper-wiki
```

升级：`codex plugin marketplace upgrade paper-wiki`，然后重新执行
`codex plugin add paper-wiki@paper-wiki`，再新开一个 task 加载新版 skill。

<details>
<summary><b>Codex 安装细节：调用方式、更新验证、SessionStart hook、分发结构</b></summary>

同一套 Codex plugin 可供 Codex app、CLI 和 IDE extension 使用。先确认当前
版本提供 plugin 命令：`codex plugin --help`。

#### 注册并安装

推荐用 CLI，步骤可复现，也适合远程开发机：

```powershell
codex plugin marketplace add Spark-To-Paper-Skills/paper-wiki
codex plugin add paper-wiki@paper-wiki
codex plugin list
```

也可以先运行第一条命令注册 marketplace，然后启动 `codex`，在 Codex
输入框输入 `/plugins`，切换到 **Paper Wiki** marketplace 并选择安装。安装完成后
请新开一个 Codex task，让新的 skill 清单进入会话。

> [!NOTE]
> `codex plugin ...` 在 PowerShell、Bash 等**终端**里运行；`/plugins` 和
> `$paper-wiki:paper-wiki` 则输入到 **Codex task 的对话框**。前半段是 plugin
> namespace，后半段是 skill 名；它不是环境变量，也不是 shell 命令。

#### 在 Codex 中调用

全局 plugin 安装后，显式入口是 `$paper-wiki:paper-wiki <action>`：

```text
$paper-wiki:paper-wiki init
$paper-wiki:paper-wiki compile
$paper-wiki:paper-wiki critique wiki/papers/example.md
$paper-wiki:paper-wiki teach "这个 wiki 中的方法分成哪几类？"
```

也可以直接用自然语言，例如："用 paper-wiki 编译当前 wiki 的新材料"。显式写
`$paper-wiki:paper-wiki` 更适合第一次使用或需要固定 action 的场景。

bootstrap 生成的项目会自带
`.agents/skills/paper-wiki-project/SKILL.md`，因此即使没有安装全局 plugin，进入
项目后也能这样调用：

```text
$paper-wiki-project wiki-init
$paper-wiki-project wiki-compile
$paper-wiki-project wiki-teach "解释这个概念"
```

#### 更新与验证

```powershell
codex plugin marketplace upgrade paper-wiki
codex plugin add paper-wiki@paper-wiki
codex plugin marketplace list --json
codex plugin list --marketplace paper-wiki --available --json
```

刷新 marketplace 后重新执行 `plugin add`，再新开 task 使用新版 skill。

#### SessionStart 更新检查与 hook 信任

plugin 内置一个 `SessionStart` 更新检查 hook（`hooks/hooks.json`）。启用后，
每次新会话会启动一个轻量后台 worker。某个已安装版本成功检查后，后续会话会在
24 小时内复用它自己的缓存；不同安装版本使用独立的
`~/.cache/paper-wiki/update-check-<version-hash>.json`，不会让 Claude Code 与 Codex
之间版本串线。首次并发启动的会话可能各自发起检查，网络或 HTTP 失败也不会写入
成功缓存，因此后续会话可能重试。hook 只保存是否有更新、已安装版本、最新版本和检查
时间，只负责提醒，不会自动下载、安装或更新任何内容；提醒中会显示对应 runtime 的
更新命令。

Codex 会自动发现 `hooks/hooks.json`，但安装或启用 plugin **不等于信任它的 hook**。
首次运行前请审查 hook，并在 Codex 的 trust 提示中明确允许；拒绝或跳过不会影响
`$paper-wiki:paper-wiki`，只是不会运行后台检查或显示更新提醒。

#### Codex 端如何分发

目前采用 **GitHub marketplace 分发**，还不是 OpenAI curated Plugins Directory
中的官方条目：

```text
GitHub 仓库
  → .agents/plugins/marketplace.json   # 让 Codex 发现 paper-wiki
  → .codex-plugin/plugin.json          # 声明插件元数据和 skills/
  → skills/paper-wiki/SKILL.md         # 提供全局 $paper-wiki:paper-wiki
  → $CODEX_HOME/plugins/cache/...      # Codex 管理的本地安装副本
```

用户只需添加一次 GitHub marketplace。仓库是发布源，cache 是 Codex 的内部安装
副本，不应手动修改。`.agents/plugins/marketplace.json` 中的 `source.path` 是
`./`，所以同一个 GitHub 仓库既是 marketplace root，也是 plugin root，不需要再维护
一份 Codex 专用 fork。新版本发布时同步更新版本号并推送仓库；用户执行上面的
`marketplace upgrade` + `plugin add` 即可更新。若以后要让用户无需先添加 GitHub
仓库、直接在公共插件目录中发现，还需要走 OpenAI 的
[plugin 提交流程](https://learn.chatgpt.com/docs/submit-plugins)。Codex plugin 与
marketplace 的官方结构说明见
[Build plugins](https://learn.chatgpt.com/docs/build-plugins)。

</details>

只想要一个自包含 wiki 的话，也可以不装 plugin：直接 `git clone` 本仓库，
用 bootstrap 脚本创建项目（[见下](#-创建双端项目)）。生成项目双端可用，
不依赖全局 plugin。

---

## 🗺️ 一套 Wiki，两端操作

一次 bootstrap，两端通吃——生成的项目双端自包含：

- `WIKI.md` 是**唯一业务规则权威**，保存 variant、schema、编译规则与禁止事项。
- `CLAUDE.md` 和 `AGENTS.md` 都是薄适配层，只负责把对应 runtime 引向
  `WIKI.md`，不各自复制规则。
- Claude Code 使用 `.claude/commands/`；Codex 使用
  `.agents/skills/paper-wiki-project/SKILL.md`。
- `research.md`、`raw/`、`wiki/` 由两端共享，切换后会看到同一份状态。

> [!IMPORTANT]
> **同一 workspace 只能有一个写入者。** 不要让 Claude Code 与 Codex 同时修改
> 同一个 wiki。切换前先等上一项任务结束，并检查工作树是否有未完成改动。

### 调用映射

7 个核心 action。Claude Code 的 `/wiki-*` 是 slash commands；它们不会在 Codex
中原样变成 slash commands。Codex 加载的是 skill，所以使用
`$paper-wiki:paper-wiki`、`$paper-wiki-project` 或自然语言点名 action。

| Action | Claude Code 项目内 | Codex 项目内 | 全局 plugin |
|---|---|---|---|
| 初始化 | `/wiki-init` | `$paper-wiki-project wiki-init` | Claude `/paper-wiki:wiki-init`；Codex `$paper-wiki:paper-wiki init` |
| 编译 | `/wiki-compile` | `$paper-wiki-project wiki-compile` | Claude `/paper-wiki:wiki-compile`；Codex `$paper-wiki:paper-wiki compile` |
| 搜论文 | `/wiki-search-latest <主题>` | `$paper-wiki-project wiki-search-latest <主题>` | Claude `/paper-wiki:wiki-search-latest`；Codex `$paper-wiki:paper-wiki search` |
| 审查 | `/wiki-critique <文件>` | `$paper-wiki-project wiki-critique <文件>` | Claude `/paper-wiki:wiki-critique`；Codex `$paper-wiki:paper-wiki critique` |
| 构思 | `/wiki-ideate <gap>` | `$paper-wiki-project wiki-ideate <gap>` | Claude `/paper-wiki:wiki-ideate`；Codex `$paper-wiki:paper-wiki ideate` |
| 查询/教学 | `/wiki-teach <问题>` | `$paper-wiki-project wiki-teach <问题>` | Claude `/paper-wiki:wiki-teach`；Codex `$paper-wiki:paper-wiki teach` |
| **自动流水线** | `/wiki-auto <文件夹>` | `$paper-wiki-project wiki-auto <文件夹>` | Claude `/paper-wiki:wiki-auto`；Codex `$paper-wiki:paper-wiki auto` |

这些 action 背后是 4 个 sub-agent：searcher、critic、ideator、cartographer。
旧的 `/wiki-ask` 是已退休的兼容别名，指向 `wiki-teach`，不计入 7 个核心 action。
`wiki-teach` 是 paper-wiki 自带的中立查询 action，两端都不需要另装 `/teach`。

---

## 🧠 LLM Wiki vs RAG

RAG 赌切分与召回；LLM Wiki 把材料真读完。

```text
RAG:   提问 → 检索片段 → 拼答案 → 质量取决于切分与召回
Wiki:  源材料 → 逐页通读 → 编译笔记 → 综合概念 → 可持续维护的知识图谱
```

| | RAG | LLM Wiki |
|---|---|---|
| **何时读** | 查询时临时检索 | 编译时完整阅读 |
| **知识形态** | 碎片向量 | 结构化笔记 + 双向链接 |
| **跨源综合** | 弱 | 概念条目 + 研究空白 |
| **可信度** | 可能断章取义 | 每条主张标注出处 |

核心铁律：`raw/` 只读且只追加；`wiki/` 可重写；每条主张都能回溯到实际读过的
源材料；wiki 没有的内容明确说 `not in wiki`，不能拿模型记忆补齐。

---

## 🔄 工作流

手动模式，你来驱动每一步：

```text
wiki-init → 导入材料 → wiki-compile → wiki-critique → wiki-ideate
                                ↓                         ↓
                         wiki-search-latest ←── 覆盖缺口 ─┘
                                ↓
                         wiki-compile → wiki-teach
```

构思走「目标 → 方向 → 探针 → idea」的螺旋。查新裁决使用六值结论——
**没有「判死」这一档**；最重的结果是一份记录在案的反方论证。
`research` 变体使用 `papers → concepts → gaps`；`course` 变体使用
`lectures + practice → topics`。Scope fence 管边界，生命周期
`BUILDING → ACTIVE → FROZEN` 管扩展节奏。

---

## 🤖 自动流水线（`/wiki-auto`）

一条命令进去，一叠评好级的 idea 卡出来。整条链无人值守：

```text
论文文件夹
  → 入库 raw/ → 批量 GPU OCR → 分批编译
  → 目标认领（problems.md）→ 方向卡
  → P0 纯 prompt 探针 → idea 卡 → 四档评级
  → 查新审查 → 止步于 SCORED
```

`/wiki-auto` 是编排者，不是裁判：它不定义任何新的 schema 或判断规则。
它的停止线是硬的——卡片绝不推过 SCORED，不跑 P1/P2 实验，不导出论文。
前置条件 fail closed：GPU 忙或缺失就干净地停下，绝无 CPU 兜底。

### 追责：给信任配留痕

无人值守的运行会做终局决策——判死、豁免、查新核验、生命周期裁定。
三套机制让这些决策可追责：

1. **INBOX。** 每个机器决策都在 `wiki/INBOX.md` 落一行只追加的记录
   （`| 日期 | 环节 | 对象 | 事项 | 状态 |`），署名 `auto` + 日期，
   诚实标注「机采标注」。事后否决任何决策只需正常编辑文件——不需要新机制。
   状态取 待人 / 已阅 / 翻案；下一次运行会为每条翻案补一条翻案回执——
   只记录，绝不自动改回。
2. **终局决策过 fresh eyes。** 评级委派给只喂卡片文件的全新上下文，必须落盘
   `wiki/ideas/<id>.tiering.md`；机器判死需要全新上下文的反方复核，落盘
   `wiki/ideas/<id>.counter.md`——为卡片续命的论证，记录在案。与主流程产物
   同一 commit 提交的工件无效：上下文切换可由 git 历史核查。
3. **八行对账。** 每次运行以固定的八行对账块收尾，每个报出的数字旁边配一条
   可重跑的 `grep`/`ls`。缺一行，这次运行就不算收尾。

idea 要拿到实验投入，必须先过查新·实据闸：① 查新裁决跑过（六值台账里有
记录），② 问题实据在手（`[p]` 探针锚点或签字豁免）。
`/wiki-auto` 整条停在闸前。

### 机械核查

| 工具 | 查什么 | 不过怎么办 |
|---|---|---|
| `scripts/idea_lint.py` | 对 idea/方向/目标卡做结构、语言、证据上限、目标卡规则检查，另加新的 T1（顶档主张的 `important_problem` 必须锚定真实的 field 层记录）与 F1（field 条目引文）两条 | 非零退出；auto 运行下机器可修一次并重新 lint，仍不过则弃稿，lint 输出原样贴进 INBOX 弃稿行 |
| `scripts/quote_check.py` | 审查指控引用的每段引文必须在编译笔记中逐字出现，抽样用确定性哈希 | 引文 MISS 把结论降级为证据不足 |

---

## 🚀 创建双端项目

```powershell
git clone https://github.com/Spark-To-Paper-Skills/paper-wiki.git
cd paper-wiki
.\scripts\bootstrap_new_wiki.ps1 -NewPath D:\my-wiki -Topic my-topic `
    -ProjectName "My Wiki" -Variant research   # 或 course
```

然后任选一端启动：

```powershell
cd D:\my-wiki
claude   # 随后运行 /wiki-init
# 或
codex    # 随后运行 $paper-wiki-project wiki-init
```

<details>
<summary><b>macOS / Linux 的 bootstrap，以及更新已有项目</b></summary>

macOS / Linux：

```bash
git clone https://github.com/Spark-To-Paper-Skills/paper-wiki.git
cd paper-wiki
bash scripts/bootstrap_new_wiki.sh --path ~/my-wiki --topic my-topic \
    --name "My Wiki" --variant research        # 或 course
```

更新已有项目：

```powershell
.\scripts\bootstrap_new_wiki.ps1 -NewPath D:\my-wiki -Update
```

```bash
bash scripts/bootstrap_new_wiki.sh --path ~/my-wiki --update
```

`-Update` / `--update` 会刷新受管的 Claude commands/agents、Codex 项目 skill、
薄适配层、manifest 和项目内协议文档；**不会覆盖** `WIKI.md`、`research.md`、
项目 `README.md`、`raw/` 或 `wiki/`。旧版 Claude-only 项目首次更新时，会先把
原完整 `CLAUDE.md` 迁移成 `WIKI.md`，再把 `CLAUDE.md` 收薄。若 variant 信息冲突，
脚本会停止，不会猜测。

</details>

完整无 GPU 示例见 [examples/QUICKSTART.md](examples/QUICKSTART.md)，逐 action
教程见 [docs/TUTORIAL.md](docs/TUTORIAL.md)，场景走读见
[docs/WALKTHROUGH.md](docs/WALKTHROUGH.md)。

---

## 🔬 OCR

扫描版、课件和图表密集 PDF 使用本地或远程 GPU OCR；不允许静默降级到 CPU。
`/wiki-auto` 同样遵守这条：GPU 忙或缺失就干净地停下，绝不换 CPU 硬跑。
Born-digital 论文可走 HTML/LaTeX 的无 OCR 路径。凭据只放环境变量，绝不能进仓库。

详见 [docs/OCR-SETUP.md](docs/OCR-SETUP.md) 与
[docs/GOTCHAS.md](docs/GOTCHAS.md)。

---

## 📁 仓库与生成项目结构

```text
paper-wiki/
├── README.md · README.en.md · LICENSE · VERSION
├── .claude-plugin/              # Claude Code marketplace 元数据
├── .codex-plugin/               # Codex plugin manifest
├── .agents/plugins/             # Codex marketplace 元数据
├── skills/paper-wiki/           # 全局 plugin skill
├── commands/                    # 8 个 slash command（含 wiki-auto）
├── agents/                      # 4 个 worker：searcher / critic / ideator / cartographer
├── hooks/                       # SessionStart 更新检查 hook
├── templates/{research,course}/ # WIKI.md + 薄 adapters + 项目 skill
├── scripts/                     # bootstrap（ps1+sh）、idea_lint、quote_check、OCR 工具
├── docs/                        # TUTORIAL.md · WALKTHROUGH.md · OCR-SETUP.md · GOTCHAS.md
│                                #   · METHODOLOGY.md · llm-wiki.protocol.yaml
│                                #   · idea-exec.contract.yaml · index.html
└── examples/                    # QUICKSTART.md + sample-research-wiki/

bootstrapped-project/
├── WIKI.md                      # 唯一业务规则权威
├── CLAUDE.md                    # Claude Code 薄适配层
├── AGENTS.md                    # Codex 薄适配层
├── research.md                  # 两端共享状态
├── .claude/{commands,agents}/   # Claude Code 项目入口
├── .agents/skills/paper-wiki-project/SKILL.md
├── .paper-wiki/                 # manifest + 自包含协议文档
├── raw/                         # 只读源材料
└── wiki/                        # 可维护的编译产物
    └── INBOX.md                 # 机器决策收件箱（首次 auto 运行生成）
```

机器契约见 [docs/llm-wiki.protocol.yaml](docs/llm-wiki.protocol.yaml)，当前版本
`llm-wiki/1.1`。

## 📄 许可证

MIT

## 🙏 致谢

- [mattpocock/skills — teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach) 启发了交互式教学方法；paper-wiki 现在把查询能力作为自身 `wiki-teach` action 提供。
- 同组织姊妹项目：[spark-to-paper-skills](https://github.com/Spark-To-Paper-Skills/spark-to-paper-skills) —— 从带评级的 idea 到一篇可投稿的论文。
- 感谢早期使用者把真实项目里的方法论与坑带回这个仓库。

---

<p align="center"><b><i>论文进。图谱出。idea 带着评级来见你。</i></b><br>
<sub>模型负责读，闸门负责狠，你只负责挑一张卡开工。</sub></p>
