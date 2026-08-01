# Output Template

Adapt this template to the request. Omit sections that do not add value.

# Project name

## Simplest correct model

Two or three sentences explaining why the project exists, what starts it, what performs the work, and what result it produces.

**Evidence boundary:** state exactly what was inspected and what remains unavailable.

## Core concepts

Explain three to five relationships the user must understand before reading implementation details.

For each concept:

- plain-language meaning;
- concrete files or components;
- common misunderstanding.

## Functional file map

```text
project/
├─ ...  # active core
├─ ...  # interfaces and integration
├─ ...  # tests
├─ ...  # documentation
└─ ...  # archive or generated material
```

Then identify the smallest set of files that explains most of the system.

## Architecture

Use a compact diagram:

```text
Input or trigger
      ↓
Control / entry point
      ↓
State and validation
      ↓
Worker / domain logic
      ↓
Result and publication
```

Name the source of truth and the important trust or failure boundaries.

## Real workflow

Use a table or numbered sequence:

| Step | Before | Action | After | Failure edge |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

Every step should name real files, functions, commands, events, or state records.

## What is easy to misunderstand

Focus on verified surprises rather than generic advice.

Examples:

- displayed configuration versus effective configuration;
- tracked status versus real-time local state;
- process completion versus business validation;
- retry safety and duplicate execution;
- current code versus outdated documentation.

## Verified, inferred, unknown

### Verified

Key facts with evidence.

### Inferred

Reasoned conclusions and their basis.

### Unknown

Missing information and the inspection needed to resolve it.

## Mental-model check

Ask two or three questions that test whether the user can reconstruct the project flow.
