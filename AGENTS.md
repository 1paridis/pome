# AGENTS.md

A collection of OpenCode agent skills for process-driven AI-assisted development. All content is Simplified Chinese.

## What this repo is

- Each skill is one directory `skills/<name>/` containing a single `SKILL.md`.
- `SKILL.md` must have YAML frontmatter with `name` and `description`. The `description` is what triggers the skill — keep it concise and state when to use it.
- Two pipelines share three stages, differing only in their starting skill:
  - Dev: `pome-seed` → `pome-plot` → `pome-grow` → `pome-reap`
  - Test: `pome-trial` → `pome-plot` → `pome-grow` → `pome-reap`

## Implementation status

`pome-seed` and `pome-trial` are implemented. `pome-plot`, `pome-grow`, and `pome-reap` are still planned. Do not assume a planned skill exists; create it before referencing it as implemented.

## `pome-seed` design contract

- `blueprint.md` uses unnumbered Markdown headings as a function tree. The root counts as level 1; the tree is at most 4 levels deep, and a parent should normally have at most 7 direct children.
- Keep the tree at user-visible or business-verifiable function granularity. Branch nodes contain headings only; every leaf contains a `功能说明` section describing what the function does, not how it is implemented.
- Determine the tree through multiple interview rounds. Ask only high-priority questions whose prerequisite decisions are settled, normally no more than 5 per round. Pause for explicit user review after the function design; do not start technical design before approval.
- Before technical design, inspect the actual project stack and related implementation. Add a concrete `技术方案` to every leaf without changing the approved function tree.
- Treat an existing `.pome/nursery/<需求简称>/blueprint.md` as protected history. Read it and wait for explicit instructions; never infer progress, fill gaps, rewrite, or modify it unprompted.

## `pome-trial` design contract

- Use `pome-trial` only for complex test needs or when the user explicitly requests a formal test design; simple low-risk checks should proceed directly without creating `test-case.md`.
- `test-case.md` uses unnumbered Markdown headings as a test design tree. Branches group test scopes or scenarios; every leaf is an independently executable and decidable test case.
- Do not impose a fixed semantic tree depth or sibling limit. Keep the tree shallow where practical, select representative combinations instead of mechanical Cartesian products, and stop decomposition at the complete test-case level.
- Every test-case leaf contains `前置条件`, `输入数据`, `执行步骤`, and `预期结果`. Branch nodes contain headings only.
- Inspect the actual requirements, implementation, and existing tests before writing concrete cases. Determine the tree through dependency-aware interview rounds and pause for explicit user review after the design.
- Treat an existing `.pome/nursery/<需求简称>/test-case.md` as protected history. A `blueprint.md` in the same directory may be read as input but must not be modified by trial.

## Conventions

- Skills write their products to `.pome/nursery/<需求简称>/` (e.g. `blueprint.md`). `<需求简称>` is a kebab-case English phrase. `nursery/` holds the currently-in-progress outputs. This is a working-output directory, not source.
- SKILL.md is written in Chinese and follows the `pome-seed` structure: frontmatter, then `# <name>`, then 输入 / 规则 / 阶段 / 产物结构 / 执行流程 sections as applicable.
- There is no build, test, or lint tooling in this repo.
