# 分层思维治理 v0.4

这是根据用户提供的《思维的层级》《思维决定人的层级》设计的项目治理 Skill。

## 当前核心

1. 不把“道”简单等同于最终目标或最高职位。
2. 不按窗口职位机械分配道、法、术。
3. 区分“处理对象的层级”和“能兼容一种还是多种”的宽度。
4. 将“道”仅转化为临时的框架超越复盘，不作为常驻 AI 权限。
5. 检查低层成功是否被误当成高层成功。
6. 所有窗口都有主要工作层级，但主要层级不是视野上限。
7. 所有窗口都应定期向上复核一至两层，同时保持决策权限边界。
8. 核心规则是：**思维可以上浮，权限不能悄悄上浮。**
9. `认知突破`只用于支持“当前思维难以独立发现自身局限，因此需要外部复核”这一原则。
10. 未使用“认知自我—认知社会”层级，也未使用道德层级。

## v0.4 新增

- 正式加入**双轮高价值收敛原则**；
- “递归二八推进法 / 两轮 96% 法”只保留为解释性别名；
- 固定 `convergence_target`、`main_chain`、`must_hold_invariants`、`acceptance_evidence` 和 `stop_condition`；
- 第一轮打通主干，第二轮只修高影响缺陷，两轮后默认关闭当前周期；
- 剩余问题分类改为 `BLOCKER / HIGH_RISK / NEXT_OBJECTIVE / DEFER / ACCEPT_RESIDUAL`；
- 新增合法动作 `CLOSE_CURRENT_CYCLE`；
- 禁止通过改名任务绕过停止复盘；
- `UPWARD_REVIEW` 增加当前收敛周期和两轮后复核；
- Kala-Agent 示例增加实际双轮收敛案例。

## v0.3 新增

- `UPWARD_REVIEW` 使用模式；
- 开始前、执行中、完成后的上浮复核流程；
- 范围扩大、连续修补、复杂度上升等触发条件；
- Codex、执行窗口、项目设计和战略窗口各自的向上复核责任；
- `templates/upward-review.md` 通用模板；
- Kala-Agent 中 Codex 向上思考但不越权的具体示例。

## 文件

- `SKILL.md`：Skill 主体
- `references/level-model.md`：六层定义、“一/多”维度和上浮复核原则
- `templates/window-role-card.md`：窗口角色卡
- `templates/cross-layer-handoff.md`：跨层交接
- `templates/upward-review.md`：任何窗口均可使用的上浮复核与双轮收敛模板
- `examples/kala-agent-window-map.md`：Kala-Agent 示例
- `agents/openai.yaml`：OpenAI/Codex 调用配置

## Codex 安装与更新

首次安装：

```powershell
npx skills add YangZihao-lab/agent-skills `
  --skill layered-thinking-governance `
  --agent codex `
  --global
```

已安装后拉取最新版本：

```powershell
npx skills update --global
```

若只想确保这个 Skill 被重新安装，也可以再次执行首次安装命令，并按当前 Skills CLI 的提示覆盖或更新。

更新后建议新建 Codex 会话，让新会话重新发现最新 Skill。

## ChatGPT 网页端更新

网页端个人 Skill 通常不会自动从 GitHub 拉取更新。

更新方式：

1. 下载最新 ZIP；
2. 在 ChatGPT Skills 页面删除或替换旧版本；
3. 上传新 ZIP；
4. 新建对话测试。

## 明确调用

```text
$layered-thinking-governance

对当前任务执行 UPWARD_REVIEW，并检查当前双轮收敛周期：保持当前职责不变，向上检查一至两层，说明当前工作服务什么目标、证明了什么、没有证明什么，当前是第一轮还是第二轮，以及是否应关闭当前周期或上报。
```
