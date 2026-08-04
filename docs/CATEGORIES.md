# Skill 领域、子类型与统一管理

本仓库用三个独立维度管理 Skill：

1. **领域（domain）**：Skill 解决哪一大类问题。
2. **子类型（subcategory）**：在该领域内采用什么工作方式。
3. **所有权（ownership）**：由本仓库维护，还是从上游固定提交镜像。

机器可读目录位于 [`catalog/skills.json`](../catalog/skills.json)。

## 当前领域

### `project-understanding` — 项目理解

帮助用户理解现有软件项目和代码库。

| 子类型 | 含义 | 当前 Skill |
|---|---|---|
| `overview-explanation` | 渐进建立整体心智模型，讲清职责、架构、状态边界和真实流程 | `project-explainer` |
| `repository-documentation` | 扫描项目并生成可长期维护的结构化文档 | `acquire-codebase-knowledge` |
| `guided-code-tour` | 通过真实文件、行号和叙事路径生成交互式导览 | `code-tour` |
| `interactive-learning` | 通过提问、预测、主动回忆和学习日志形成长期理解 | `learn-codebase` |

### `project-governance` — 项目治理

帮助多窗口和多 Agent 项目区分问题层级、权限边界、方法论与执行，检查目标漂移，并降低项目结构和维护面的认知负荷。

| 子类型 | 含义 | 当前 Skill |
|---|---|---|
| `layered-governance` | 按物、事、器、术、法路由问题，检查低层成果冒充高层成功，并支持跨层交接和临时框架释放复盘 | `layered-thinking-governance` |
| `structural-simplification` | 在每次新增前检查需要、替代和归宿，并通过生成核、单一真相源和可逆剃刀简化长期结构 | `project-razor` |

```text
项目治理
├─ 分层思维治理     layered-thinking-governance
└─ 结构断舍离       project-razor
```

## 后续扩展方式

以后增加不同用途的 Skill 时，应先判断它是否属于现有领域；只有确实解决另一大类问题时，才新增顶层领域。不会在没有实际 Skill 时提前创建空分类。

## 所有权类型

### `first-party`

由本仓库直接维护：

- 可以在本仓库修改；
- 不包含 `_UPSTREAM.json`；
- 必须在 `catalog/skills.json` 登记；
- 变更需同步更新说明、元数据和校验。

当前 Skill：

- `project-explainer`
- `layered-thinking-governance`
- `project-razor`

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

`project-explainer` 关闭隐式调用，避免普通开发任务被讲解流程打断。

`layered-thinking-governance` 允许隐式调用，适用于项目规划、窗口分工、跨层交接和目标漂移审查。

`project-razor` 也允许隐式调用，但隐式模式严格限制为只读的 `PRE_ACTION_RAZOR`：

- 在新增或长期保留结构前检查需要、替代、生命周期、生成核和认知成本；
- 没有问题时可以静默通过；
- 不自动发起全仓库清理；
- 不移动、合并、归档、删除或恢复任何内容；
- 所有实际处置仍需用户明确批准精确计划。

## 默认副作用

| Skill | 默认效果 |
|---|---|
| `project-explainer` | 只读 |
| `layered-thinking-governance` | 只读 |
| `project-razor` | 只读；隐式仅作动作前检查，执行清理需用户批准精确计划 |
| `acquire-codebase-knowledge` | 写入 `docs/codebase/` |
| `code-tour` | 写入 `.tours/` |
| `learn-codebase` | 写入 `.claude/learning-journal.md` |

安装 Skill 不会自动执行写入或清理；只有 Agent 按 Skill 流程工作并获得相应授权时才可能发生。

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
