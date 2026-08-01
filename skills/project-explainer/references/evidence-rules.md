# Evidence Rules

Use explicit evidence labels when the distinction matters.

## Evidence classes

### VERIFIED

Directly supported by material actually inspected in the current session:

- source code or configuration;
- tests;
- Git history or pull request diff;
- structured status or result file;
- local process or filesystem inspection;
- authoritative external documentation.

State the relevant path, function, commit, event, or source.

### INFERRED

A conclusion logically derived from verified evidence but not directly observed. State the basis and use language such as "this implies" or "the code appears to".

Do not promote an inference to fact merely because it is likely.

### UNKNOWN

Information that cannot be established from available evidence. Explain what evidence would resolve it.

Never fill an unknown with a plausible story.

## Evidence priority

When sources conflict, use this order as a starting point:

1. current runtime observation for current runtime state;
2. current executable code and configuration;
3. tests that exercise the relevant behavior;
4. current structured artifacts and recent Git history;
5. architecture and protocol documentation;
6. README and prose descriptions;
7. comments and names;
8. assumptions.

The order is contextual: a specification can be authoritative for intended behavior while code is authoritative for actual behavior. Report the divergence.

## Remote versus local boundaries

A connected Git repository normally proves only tracked repository content and Git history. It does not prove the current contents of:

- ignored directories such as `local/`, `logs/`, `tmp/`, or `.env`;
- uncommitted changes;
- running processes and PIDs;
- scheduled task state;
- local credentials;
- generated runtime artifacts;
- local configuration that is intentionally excluded from Git.

When only Git is available, phrase local behavior as code-defined behavior, not current machine state.

## History versus current state

A historical commit proves that an event was recorded in Git. It does not automatically prove:

- the process is still running;
- the same configuration remains active;
- a local file still exists;
- a branch is still deployed;
- the published result matches an untracked local artifact.

Use timestamps and branch context, and separate "recorded then" from "true now".

## Sensitive material

Do not reproduce:

- credentials or tokens;
- private source text not required for explanation;
- raw logs containing user prompts, personal data, or secrets;
- absolute local paths when a repository-relative path is sufficient;
- hidden reasoning or internal model traces.

Summarize safely while retaining the technical meaning.

## Citation discipline

When citations are supported:

- place them immediately after the claim they support;
- cite the smallest useful source range;
- do not cite a file merely because it is related;
- cite conflicting sources separately;
- avoid claiming completeness unless a complete tree or exhaustive search was actually obtained.
