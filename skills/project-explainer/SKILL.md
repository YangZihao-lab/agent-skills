---
name: project-explainer
description: >
  Explain an existing software repository to its owner or a non-expert by building
  a verified mental model, grouping files by responsibility, mapping architecture,
  and tracing a real workflow through actual files and state changes. Use only when
  the user explicitly asks to understand, map, tour, or learn a project. Do not use
  for routine coding, bug fixes, implementation, or narrow code edits.
disable-model-invocation: true
---

# Project Explainer

Help the user understand a real software project without pretending that a file dump is an explanation.

## Default contract

- Work read-only unless the user explicitly requests generated documentation or tour files.
- Do not modify source code, configuration, Git state, issues, or pull requests while explaining.
- Use the user's language and calibrate technical depth to their demonstrated background.
- Prefer a progressive explanation over a large one-shot report.
- Separate verified facts, reasoned inferences, and unknowns.
- Never treat Git-visible files as proof of untracked local runtime state.
- Never claim to have inspected files, branches, logs, processes, or configuration that were not actually read.

Load these references as needed:

- [`references/explanation-flow.md`](references/explanation-flow.md) for the required teaching sequence.
- [`references/evidence-rules.md`](references/evidence-rules.md) for evidence labels and remote/local boundaries.
- [`references/output-template.md`](references/output-template.md) for the standard answer structure.

## Determine the target

1. Resolve the repository or project from the current workspace, connected source, uploaded files, or the user's explicit name.
2. Ask one clarifying question only when the target cannot be resolved safely.
3. State the evidence boundary before detailed explanation, for example:
   - repository files only;
   - repository plus Git history;
   - local workspace including ignored files;
   - uploaded snapshot only.

## Choose a mode

Infer the narrowest mode that satisfies the request:

- **Overview** — project purpose, core concepts, functional file map, architecture, risks.
- **Workflow trace** — follow one real command, request, event, or user action end to end.
- **Component deep dive** — explain one subsystem and its interfaces.
- **Learning session** — teach interactively with short prediction and recall checks.
- **Documentation mode** — create durable docs only when explicitly requested.

When the user asks generally to understand a project, use Overview first, then continue with one Workflow trace.

## Required workflow

### 1. Establish project intent

Read the README and other intent documents before implementation details. Summarize:

- what problem the project solves;
- who or what uses it;
- what a successful run produces;
- what the project explicitly does not do.

Cross-check stated intent against actual files and entry points. Mark divergence instead of smoothing it over.

### 2. Build a functional file map

List the complete tracked tree when practical, but explain it by responsibility rather than alphabetically. Use these buckets when applicable:

- entry points and orchestration;
- domain or business logic;
- data and state;
- integrations and interfaces;
- operations and deployment;
- tests and verification;
- documentation;
- generated or archived material;
- local or ignored runtime material that is known to exist.

Identify the smallest set of files that explains most of the system. Do not explain every file with equal weight.

### 3. Teach the core concepts

Before walking through implementation, define three to five concepts the user must understand. Connect each concept to concrete files. Avoid jargon without a plain-language definition.

### 4. Map architecture and boundaries

Explain modules, ownership boundaries, inputs, outputs, state stores, processes, and external systems. Use a compact diagram when it improves understanding.

Explicitly identify when applicable:

- source of truth;
- control plane versus execution plane;
- durable versus transient state;
- trusted versus untrusted inputs;
- synchronous versus asynchronous boundaries;
- failure and recovery boundaries.

### 5. Trace a real workflow

Choose an existing, evidenced workflow rather than inventing a hypothetical one. Follow it through:

1. trigger;
2. input files or request;
3. ingestion and validation;
4. state transition;
5. execution;
6. intermediate events or artifacts;
7. result validation;
8. publication or response;
9. final durable state.

At every step name the relevant file, function, process, or state record. Distinguish observed history from behavior inferred from code.

### 6. Explain failure modes and surprises

Prioritize what a project owner is likely to misunderstand:

- a field that is displayed but not actually enforced;
- a status file that is not real-time state;
- a success condition based only on process exit;
- destructive queue behavior;
- stale local state after a crash;
- broad filesystem or network permissions;
- documentation that lags implementation;
- generated or ignored files mistaken for tracked source.

Do not manufacture concerns to fill a template.

### 7. Check understanding

End substantial explanations with two or three concrete recall questions, unless the user asked for a reference-only report. Questions should test the system's actual mental model, not syntax trivia.

## Output discipline

- Start with the simplest correct model.
- Expand one layer at a time.
- Keep file paths exact and repository-relative when possible.
- Cite concrete source locations when the environment supports citations.
- Use small tables only when comparison is genuinely clearer.
- Avoid unexplained acronyms and long undifferentiated bullet lists.
- Never expose secrets, credentials, private source text, or raw sensitive logs.

## Writing files

Remain read-only by default. When the user explicitly requests durable output:

- place project explanations under `docs/codebase/` unless the project has an established documentation convention;
- place CodeTour files under `.tours/`;
- show the proposed files before modifying a protected or production repository when normal workflow requires approval;
- do not overwrite existing documentation without comparing and preserving useful content.

## Completion criteria

A successful explanation leaves the user able to state:

1. why the project exists;
2. which files and modules matter most;
3. where authoritative state lives;
4. how one real workflow moves through the system;
5. where failures can occur and how recovery works;
6. which conclusions are verified and which remain unknown.
