# Agent Skills 仓库约定

本仓库集中管理可移植的 Agent Skills，并以 `catalog/skills.json` 作为统一目录。

## 所有权边界

- `skills/` 下带 `_UPSTREAM.json` 的目录属于 `mirrored-upstream`，由同步脚本生成，不得直接修改。
- 更新第三方 Skill 时，只修改 `upstream-skills.json` 中的固定提交，再运行同步。
- 必须保留上游许可证和来源；不得导入许可证不明确或不兼容的内容。
- 自建 Skill 属于 `first-party`，直接放入 `skills/<name>/`，不得添加 `_UPSTREAM.json`。
- 对第三方 Skill 的本地改造应建立新的 First-party Skill 名称，不要篡改镜像目录。

## 统一目录

- 每个 `skills/<name>/SKILL.md` 都必须在 `catalog/skills.json` 登记。
- 每个目录条目必须声明：分类、所有权、状态、调用策略、默认副作用、是否包含脚本和支持平台。
- Skill 名称、目录名与 `SKILL.md` frontmatter 的 `name` 必须一致。
- 分类必须先在 `catalog/skills.json` 的 `categories` 中定义，并同步说明到 `docs/CATEGORIES.md`。
- 删除或重命名 Skill 时，必须同时更新目录、README、来源锁文件和相关文档。

## First-party Skill

- 默认采用只读和最小权限设计；需要写文件或执行命令时必须在 `SKILL.md` 明确说明。
- 面向 Codex 的界面元数据放在 `agents/openai.yaml`，并保持与 `SKILL.md` 一致。
- 只希望显式调用的 Skill，应设置 `policy.allow_implicit_invocation: false`，并在文档中说明使用技能选择器或 `$skill-name`。
- 参考资料放在 `references/`，确定性工具放在 `scripts/`，输出模板放在 `assets/`。
- 不为简单提示词增加不必要的脚本或依赖。

## 安全与验证

- 默认不执行上游脚本；同步过程只复制文件。
- 不提交凭据、私有项目源码、聊天记录、原始敏感日志或本机绝对路径。
- 新增、删除、移动或更新 Skill 后必须运行：

```powershell
python scripts/validate_catalog.py
```

- 修改同步脚本后还必须运行：

```powershell
python -m py_compile scripts/sync_upstream.py scripts/validate_catalog.py
```

- 校验失败不得合并到 `main`。
