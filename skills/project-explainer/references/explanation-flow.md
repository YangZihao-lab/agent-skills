# Explanation Flow

Use this sequence to turn repository evidence into a usable mental model.

## Phase 1: Orient

1. State the evidence boundary: Git repository, local workspace, uploaded snapshot, or connected source.
2. Read the root README and project-level instruction files.
3. Identify the project purpose, user, input, and output.
4. Compare stated intent with actual entry points and active files.

Output: a two- or three-sentence simplest correct model.

## Phase 2: Map

1. Obtain the complete tracked file tree when practical.
2. Separate active code from tests, documentation, generated output, and archives.
3. Identify ignored or local runtime files only when evidence proves they exist.
4. Select the smallest set of files that explains most of the system.

Output: a functional file map, not an alphabetical dump.

## Phase 3: Build the mental model

Explain three to five concepts before implementation details. A concept should describe a relationship the user must understand, for example:

- command envelope versus instruction body;
- control plane versus worker;
- tracked status versus local runtime state;
- process success versus business success;
- durable queue versus transient process memory.

Each concept must point to concrete evidence.

## Phase 4: Trace

Choose a real workflow with evidence in code, history, logs, fixtures, tests, or status artifacts. Follow it through trigger, ingestion, state, execution, validation, publication, and recovery.

Use this per-step structure:

1. **Before** — relevant files or state before the step.
2. **Action** — function, process, command, request, or event.
3. **After** — files or state after the step.
4. **Why it matters** — implication for the project owner.
5. **Failure edge** — what can fail at this boundary.

## Phase 5: Stress the model

Explain the most important non-obvious behaviors:

- what is authoritative;
- what is only a display or cache;
- what survives restart;
- what can be lost during a crash;
- what is retried;
- what can be duplicated;
- what permissions are broad;
- which docs do not match code.

Do not add generic risks that are unsupported by this project.

## Phase 6: Verify learning

Ask two or three questions that require the user to reconstruct the workflow. Good questions compare two easily confused components or ask what happens after a failure.

Do not quiz syntax, line numbers, or incidental implementation details.

## Mode matrix

| Mode | Required phases | Writes files |
|---|---|---|
| Overview | 1, 2, 3, 5 | No |
| Workflow trace | 1, 3, 4, 5 | No |
| Component deep dive | 1, 2, 3, 4 | No |
| Learning session | 1–6, delivered interactively | Journal only if explicitly requested |
| Documentation | 1–5 | Only after explicit request |
