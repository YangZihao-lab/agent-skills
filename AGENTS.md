# Agent Skills 仓库约定

本仓库集中管理可移植的 Agent Skills。

- `skills/` 下带 `_UPSTREAM.json` 的目录由同步脚本生成，不得直接修改。
- 更新第三方 Skill 时，只修改 `upstream-skills.json` 中的固定提交，再运行同步。
- 必须保留上游许可证和来源；不得导入许可证不明确或不兼容的内容。
- 自建 Skill 可以直接放入 `skills/<name>/`，但不得添加 `_UPSTREAM.json`。
- 每个 Skill 必须包含 `SKILL.md`，名称与目录名应一致。
- 默认不执行上游脚本；同步过程只复制文件。
- 不提交凭据、私有项目源码、聊天记录或本机绝对路径。
- 对第三方 Skill 的本地改造应建立独立 Skill 名称，不要篡改镜像目录。
