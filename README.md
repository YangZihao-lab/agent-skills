# Agent Skills

个人 Agent Skills 汇总仓库。GitHub 是唯一版本源；本地 Codex、Cursor、Claude Code 等兼容 Agent 可通过 Skills CLI 安装，ChatGPT 网页端可以读取或上传同一份 Skill。

## 管理模型

仓库从三个维度统一管理 Skill：

- **领域（domain）**：解决哪一大类问题。
- **子类型（subcategory）**：在该领域内采用什么工作方式。
- **所有权（ownership）**：本仓库直接维护，或从上游固定提交镜像。

所有权分为：

- **First-party**：本仓库直接维护，可以修改和迭代。
- **Mirrored upstream**：从第三方仓库固定 Git 提交同步，不直接修改镜像目录。

机器可读的统一目录位于 [`catalog/skills.json`](catalog/skills.json)，领域、子类型和维护规则见 [`docs/CATEGORIES.md`](docs/CATEGORIES.md)。

## 当前收录

当前四个 Skill 全都属于同一个顶层领域：**项目理解**。区别只是讲解和学习方式不同。

| Skill | 领域 | 子类型 | 默认效果 | 所有权 | 来源 |
|---|---|---|---|---|---|
| `project-explainer` | 项目理解 | 总览讲解 | 只读 | First-party | 本仓库 |
| `acquire-codebase-knowledge` | 项目理解 | 项目文档化 | 写入 `docs/codebase/` | Mirrored upstream | `github/awesome-copilot` |
| `code-tour` | 项目理解 | 代码导览 | 写入 `.tours/` | Mirrored upstream | `github/awesome-copilot` |
| `learn-codebase` | 项目理解 | 互动教学 | 写入 `.claude/learning-journal.md` | Mirrored upstream | `ktaletsk/learn-codebase` |

```text
项目理解
├─ 总览讲解         project-explainer
├─ 项目文档化       acquire-codebase-knowledge
├─ 代码导览         code-tour
└─ 互动教学         learn-codebase
```

以后可以并列增加真正不同的顶层领域，例如软件开发、代码审查、研究分析、写作、自动化、数据分析或运维发布；每个领域再定义自己的子类型。不会在没有实际 Skill 时预先创建空领域。

### 推荐入口：`project-explainer`

用于从项目所有者视角理解现有仓库：

1. 解释项目为什么存在；
2. 按职责整理完整文件地图；
3. 建立三到五个核心概念；
4. 说明架构、状态来源和边界；
5. 沿一条真实任务追踪文件与状态变化；
6. 区分已验证事实、推断和未知信息；
7. 解释故障与恢复路径；
8. 用简短问题检查是否真正理解。

它默认只读，并在 Codex 中关闭隐式调用。需要通过技能选择器或 `$project-explainer` 明确调用，不会自动干扰普通开发任务。

## 本地安装

列出仓库中的 Skill：

```powershell
npx skills add YangZihao-lab/agent-skills --list
```

全局安装 `project-explainer` 到 Codex：

```powershell
npx skills add YangZihao-lab/agent-skills `
  --skill project-explainer `
  --agent codex `
  --global
```

使用：

```text
$project-explainer

讲解当前项目。先建立整体心智模型，再沿一条真实任务解释文件和状态变化。
```

安装其他 Skill：

```powershell
npx skills add YangZihao-lab/agent-skills `
  --skill acquire-codebase-knowledge `
  --agent codex `
  --global
```

更新已安装 Skill：

```powershell
npx skills update --global
```

具体参数以当前 Skills CLI 为准。

## ChatGPT 网页端

网页端可以通过已连接的 GitHub 临时读取：

```text
读取 YangZihao-lab/agent-skills/skills/project-explainer/SKILL.md，
按照该流程讲解 YangZihao-lab/Control。
```

也可以下载对应 Skill 文件夹并上传到 ChatGPT 的「技能」页面。网页端和本地 Agent 不会自动共享安装状态，但都以本仓库为版本源。

## 上游同步

`upstream-skills.json` 是第三方来源锁文件。修改其中的 `source_ref` 后，GitHub Actions 会重新抓取固定提交并更新 `skills/`。

每个镜像 Skill 都包含：

- `_UPSTREAM.json`：来源仓库、固定提交和原路径；
- 上游许可证；
- 完整的 `SKILL.md`、脚本、模板与参考资料。

本地也可以运行：

```powershell
python scripts/sync_upstream.py
```

同步程序只执行 Git 拉取和文件复制，不执行任何上游 Skill 脚本。

## 校验

统一目录必须覆盖 `skills/` 下的每一个可安装 Skill：

```powershell
python scripts/validate_catalog.py
```

校验包括：

- Skill 目录名与 `SKILL.md` 的 `name` 一致；
- 每个 Skill 都有目录条目；
- 顶层领域存在且不重复；
- 子类型存在、唯一且属于正确领域；
- Skill 的领域和子类型关系正确；
- First-party 与镜像目录边界正确；
- 镜像 Skill 已登记在 `upstream-skills.json`；
- 脚本声明与真实目录一致；
- `project-explainer` 保持显式调用策略。

GitHub Actions 会在 Pull Request 和 `main` 更新时自动执行校验。

## 目录

```text
agent-skills/
├─ skills/
│  ├─ project-explainer/            # First-party
│  ├─ acquire-codebase-knowledge/   # Mirrored upstream
│  ├─ code-tour/                    # Mirrored upstream
│  └─ learn-codebase/               # Mirrored upstream
├─ catalog/skills.json              # 领域、子类型和 Skill 机器目录
├─ docs/CATEGORIES.md               # 分类和所有权规则
├─ scripts/sync_upstream.py         # 固定提交镜像
├─ scripts/validate_catalog.py      # 目录和边界校验
├─ upstream-skills.json             # 第三方来源锁文件
├─ AGENTS.md                        # 仓库维护约定
└─ LICENSE
```

## 安全与许可证

安装第三方 Skill 前应检查其 `SKILL.md`、`scripts/` 和权限要求。Skill 被安装并调用后，可能运行命令或修改文件；本仓库收录不等于安全背书。

本仓库自身采用 MIT License。镜像的第三方 Skill 继续适用各自的上游许可证。
