# Agent Skills

个人 Agent Skills 汇总仓库。GitHub 是唯一版本源；本地 Codex、Cursor、Claude Code 等兼容 Agent 可通过 Skills CLI 安装，ChatGPT 网页端可以读取或上传同一份 Skill。

## 当前收录

| Skill | 用途 | 来源 |
|---|---|---|
| `acquire-codebase-knowledge` | 扫描现有代码库并生成技术栈、结构、架构、测试、集成和风险文档 | `github/awesome-copilot` |
| `code-tour` | 生成按真实文件和行号导航的 VS Code CodeTour | `github/awesome-copilot` |
| `learn-codebase` | 通过苏格拉底提问、主动回忆和学习日志理解代码库 | `ktaletsk/learn-codebase` |

第三方 Skill 固定到 `upstream-skills.json` 中记录的 Git 提交。镜像目录包含 `_UPSTREAM.json` 和上游许可证，不应直接修改。

## 安装

列出仓库中的 Skill：

```powershell
npx skills add YangZihao-lab/agent-skills --list
```

全局安装一个 Skill 到 Codex：

```powershell
npx skills add YangZihao-lab/agent-skills `
  --skill acquire-codebase-knowledge `
  --agent codex `
  --global
```

安装项目教学 Skill：

```powershell
npx skills add YangZihao-lab/agent-skills `
  --skill learn-codebase `
  --agent codex `
  --global
```

更新已安装 Skill：

```powershell
npx skills update --global
```

具体参数以当前 Skills CLI 为准。

## ChatGPT 网页端

网页端可以通过已连接的 GitHub 读取：

```text
YangZihao-lab/agent-skills/skills/<skill-name>/SKILL.md
```

也可以将对应 Skill 文件夹下载后上传到 ChatGPT 的「技能」页面。网页端和本地 Agent 不会自动共享安装状态，但都以本仓库内容为源。

## 上游同步

`upstream-skills.json` 是来源锁文件。修改其中的 `source_ref` 后，GitHub Actions 会重新抓取固定提交并更新 `skills/`。

本地也可以运行：

```powershell
python scripts/sync_upstream.py
```

同步程序只执行 Git 拉取和文件复制，不执行任何上游 Skill 脚本。

## 目录

```text
agent-skills/
├─ skills/                    # 可安装的 Skill
├─ scripts/sync_upstream.py   # 可重复的镜像脚本
├─ upstream-skills.json       # 上游来源和固定提交
├─ AGENTS.md                  # 维护规则
└─ LICENSE
```

## 安全与许可证

安装第三方 Skill 前应检查其 `SKILL.md`、`scripts/` 和权限要求。Skill 被安装并调用后，可能运行命令或修改文件；本仓库收录不等于安全背书。

本仓库自身采用 MIT License。镜像的第三方 Skill 继续适用各自的上游许可证。
