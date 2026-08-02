# Agent Skills

个人 Agent Skills 汇总仓库。GitHub 是唯一版本源；本地 Codex、Cursor、Claude Code 等兼容 Agent 可通过 Skills CLI 安装，ChatGPT 网页端可以读取或上传同一份 Skill。

## 管理模型

仓库从三个维度统一管理 Skill：

- **领域（domain）**：解决哪一大类问题。
- **子类型（subcategory）**：在该领域内采用什么工作方式。
- **所有权（ownership）**：本仓库直接维护，或从上游固定提交镜像。

机器可读目录位于 [`catalog/skills.json`](catalog/skills.json)，领域、子类型和维护规则见 [`docs/CATEGORIES.md`](docs/CATEGORIES.md)。

## 当前收录

当前包含两个顶层领域：**项目理解**与**项目治理**。

| Skill | 领域 | 子类型 | 默认效果 | 调用 | 所有权 |
|---|---|---|---|---|---|
| `project-explainer` | 项目理解 | 总览讲解 | 只读 | 显式 | First-party |
| `acquire-codebase-knowledge` | 项目理解 | 项目文档化 | 写入 `docs/codebase/` | 可隐式 | Mirrored upstream |
| `code-tour` | 项目理解 | 代码导览 | 写入 `.tours/` | 可隐式 | Mirrored upstream |
| `learn-codebase` | 项目理解 | 互动教学 | 写入 `.claude/learning-journal.md` | 显式 | Mirrored upstream |
| `layered-thinking-governance` | 项目治理 | 分层思维治理 | 只读 | 可隐式 | First-party |
| `project-razor` | 项目治理 | 结构断舍离 | 只读 | 显式 | First-party |

```text
项目理解
├─ 总览讲解         project-explainer
├─ 项目文档化       acquire-codebase-knowledge
├─ 代码导览         code-tour
└─ 互动教学         learn-codebase

项目治理
├─ 分层思维治理     layered-thinking-governance
└─ 结构断舍离       project-razor
```

## 主要 Skill

### `project-explainer`

从项目所有者视角理解现有仓库：解释项目目的、文件职责、架构、真实工作流、状态来源和故障边界。默认只读并关闭隐式调用。

### `layered-thinking-governance`

按“物、事、器、术、法”判断当前问题、窗口权限和上报边界，检查低层成果是否被误当成高层成功，并在目标漂移时进行临时框架释放复盘。默认只读，允许隐式调用。

### `project-razor`

通过断舍离、单一真相源和可逆剃刀，简化项目目录、文档、分支、工具、协议和工作流，减少新窗口与用户需要同时记住的内容。

它默认只读并关闭隐式调用。任何移动、合并、归档或删除都必须先展示精确计划，并获得用户明确批准。

## 本地安装

列出仓库中的 Skill：

```powershell
npx skills add YangZihao-lab/agent-skills --list
```

安装到 Codex：

```powershell
npx skills add YangZihao-lab/agent-skills `
  --skill layered-thinking-governance `
  --agent codex `
  --global

npx skills add YangZihao-lab/agent-skills `
  --skill project-razor `
  --agent codex `
  --global
```

明确调用：

```text
$layered-thinking-governance

按层级审查当前项目，检查是否越级或发生目标漂移。
```

```text
$project-razor

对当前仓库执行 QUICK_RAZOR，只读，指出最影响理解的五个复杂度来源。
```

更新已安装 Skill：

```powershell
npx skills update --global
```

具体参数以当前 Skills CLI 为准。

## ChatGPT 网页端

网页端可以通过已连接的 GitHub 临时读取：

```text
读取 YangZihao-lab/agent-skills/skills/project-razor/SKILL.md，
按照该 Skill 对目标仓库执行只读结构审计。
```

也可以下载对应 Skill 文件夹并上传到 ChatGPT 的「技能」页面。网页端和本地 Agent 不会自动共享安装状态，但都以本仓库为版本源。

## 上游同步

`upstream-skills.json` 是第三方来源锁文件。修改其中的 `source_ref` 后，GitHub Actions 会重新抓取固定提交并更新 `skills/`。

本地也可以运行：

```powershell
python scripts/sync_upstream.py
```

同步程序只执行 Git 拉取和文件复制，不执行任何上游 Skill 脚本。

## 校验

```powershell
python scripts/validate_catalog.py
```

校验包括 Skill 目录、目录登记、领域与子类型、所有权边界、脚本声明和调用策略。GitHub Actions 会在 Pull Request 和 `main` 更新时自动执行校验。

## 目录

```text
agent-skills/
├─ skills/
│  ├─ project-explainer/               # First-party
│  ├─ layered-thinking-governance/     # First-party
│  ├─ project-razor/                   # First-party
│  ├─ acquire-codebase-knowledge/      # Mirrored upstream
│  ├─ code-tour/                       # Mirrored upstream
│  └─ learn-codebase/                  # Mirrored upstream
├─ catalog/skills.json
├─ docs/CATEGORIES.md
├─ scripts/sync_upstream.py
├─ scripts/validate_catalog.py
├─ upstream-skills.json
├─ AGENTS.md
└─ LICENSE
```

## 安全与许可证

安装第三方 Skill 前应检查其 `SKILL.md`、脚本和权限要求。Skill 被安装并调用后，可能运行命令或修改文件；本仓库收录不等于安全背书。

本仓库自身采用 MIT License。镜像的第三方 Skill 继续适用各自的上游许可证。
