# Skill 领域、子类型与统一管理

本仓库用三个独立维度管理 Skill：

1. **领域（domain）**：Skill 解决哪一大类问题。
2. **子类型（subcategory）**：在该领域内采用什么工作方式。
3. **所有权（ownership）**：由本仓库维护，还是从上游固定提交镜像。

机器可读目录位于 [`catalog/skills.json`](../catalog/skills.json)。

## 当前领域

### `project-understanding` — 项目理解

当前收录的四个 Skill 全都属于同一个顶层领域：帮助用户理解现有软件项目和代码库。

它们不是四个并列的顶层分类，而是四种不同的讲解或学习方式。

| 子类型 | 含义 | 当前 Skill |
|---|---|---|
| `overview-explanation` | 渐进建立整体心智模型，讲清职责、架构、状态边界和真实流程 | `project-explainer` |
| `repository-documentation` | 扫描项目并生成可长期维护的结构化文档 | `acquire-codebase-knowledge` |
| `guided-code-tour` | 通过真实文件、行号和叙事路径生成交互式导览 | `code-tour` |
| `interactive-learning` | 通过提问、预测、主动回忆和学习日志形成长期理解 | `learn-codebase` |

因此当前逻辑是：

```text
项目理解
├─ 总览讲解         project-explainer
├─ 项目文档化       acquire-codebase-knowledge
├─ 代码导览         code-tour
└─ 互动教学         learn-codebase
```

## 后续扩展方式

以后增加不同用途的 Skill 时，应先判断它是否属于现有领域；只有确实解决另一大类问题时，才新增顶层领域。

可能出现的未来领域示例：

```text
软件开发
代码质量与审查
研究与分析
写作与内容生产
工作流自动化
数据分析
运维与发布
```

这些只是扩展方向，不会在没有实际 Skill 时提前写进机器目录，避免空分类和失控增长。

每个新领域可以继续拥有自己的子类型。例如：

```text
软件开发
├─ 功能实现
├─ 缺陷修复
├─ 重构
└─ 测试生成

研究与分析
├─ 资料检索
├─ 证据审定
├─ 对比分析
└─ 报告生成
```

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
3. 判断所属顶层领域；不存在时才新增 `domains` 条目。
4. 判断领域内的子类型；不存在时新增 `subcategories` 条目并指向正确领域。
5. 在 `catalog/skills.json` 登记领域、子类型、所有权、调用策略、默认副作用和平台。
6. 第一方 Skill 不得包含 `_UPSTREAM.json`。
7. 镜像 Skill 必须通过 `upstream-skills.json` 管理并保留许可证。
8. 若提供 `agents/openai.yaml`，确保界面文案和调用策略与 `SKILL.md` 一致。
9. 运行：

```powershell
python scripts/validate_catalog.py
```
