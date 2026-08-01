# Skill 分类与统一管理

本仓库用两个维度管理 Skill：**用途分类**和**所有权类型**。机器可读目录位于 [`catalog/skills.json`](../catalog/skills.json)。

## 用途分类

### `codebase-understanding` — 代码库理解

目标是帮助项目所有者建立整体心智模型，不以生成代码为主要目的。

典型输出：

- 项目为什么存在；
- 功能化文件地图；
- 核心概念和架构边界；
- 一条真实工作流；
- 故障与恢复边界；
- 理解检查。

当前 Skill：

- `project-explainer`

### `codebase-documentation` — 代码库文档与导览

目标是生成可保留、可维护、可导航的项目资料。

典型输出：

- `docs/codebase/` 文档；
- `.tours/*.tour`；
- 技术栈、结构、架构、测试和风险说明。

当前 Skill：

- `acquire-codebase-knowledge`
- `code-tour`

### `guided-learning` — 互动学习

目标是通过预测、提问、主动回忆和复习记录形成长期理解。

当前 Skill：

- `learn-codebase`

## 所有权类型

### `first-party`

由本仓库直接维护：

- 可以在本仓库修改；
- 不包含 `_UPSTREAM.json`；
- 必须在 `catalog/skills.json` 登记；
- 变更需同步更新说明、元数据和校验。

当前 Skill：

- `project-explainer`

### `mirrored-upstream`

由第三方仓库固定提交镜像：

- 目录包含 `_UPSTREAM.json`；
- 不得直接修改镜像目录；
- 版本由 `upstream-skills.json` 锁定；
- 更新时修改来源提交并运行同步；
- 必须保留上游许可证。

当前 Skill：

- `acquire-codebase-knowledge`
- `code-tour`
- `learn-codebase`

## 调用策略

- `explicit`：只应由用户明确选择或使用 `$skill-name` 调用。
- `implicit-eligible`：Agent 可以根据 Skill 描述自动匹配；安装前应检查描述是否过宽。

`project-explainer` 在 Codex 中通过 `agents/openai.yaml` 设置：

```yaml
policy:
  allow_implicit_invocation: false
```

因此它不会进入普通开发任务的自动匹配路径。显式使用时应通过技能选择器或 `$project-explainer`。

## 默认副作用

目录记录每个 Skill 的默认写入行为：

| Skill | 默认效果 |
|---|---|
| `project-explainer` | 只读 |
| `acquire-codebase-knowledge` | 写入 `docs/codebase/` |
| `code-tour` | 写入 `.tours/` |
| `learn-codebase` | 写入 `.claude/learning-journal.md` |

安装 Skill 不会自动执行这些行为；只有 Skill 被调用且 Agent 按其流程工作时才可能发生。

## 新增 Skill 检查表

1. 在 `skills/<name>/` 添加有效的 `SKILL.md`。
2. 名称必须与目录名一致。
3. 在 `catalog/skills.json` 登记分类、所有权、调用策略、默认副作用和平台。
4. 第一方 Skill 不得包含 `_UPSTREAM.json`。
5. 镜像 Skill 必须通过 `upstream-skills.json` 管理并保留许可证。
6. 若提供 `agents/openai.yaml`，确保界面文案和调用策略与 `SKILL.md` 一致。
7. 运行：

```powershell
python scripts/validate_catalog.py
```
