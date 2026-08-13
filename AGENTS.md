# AGENTS.md

A collection of OpenCode agent skills for process-driven AI-assisted development. All content is Simplified Chinese.

## What this repo is

- Each skill is one directory `skills/<name>/` containing a single `SKILL.md`.
- `SKILL.md` must have YAML frontmatter with `name` and `description`. The `description` is what triggers the skill — keep it concise and state when to use it.
- Two pipelines share three stages, differing only in their starting skill:
  - Dev: `pome-seed` → `pome-plot` → `pome-grow` → `pome-reap`
  - Test: `pome-trial` → `pome-plot` → `pome-grow` → `pome-reap`

## Important: only `pome-seed` exists yet

README.md describes 5 skills, but only `skills/pome-seed/SKILL.md` is implemented. `pome-trial`, `pome-plot`, `pome-grow`, `pome-reap` are planned but not written. Do not assume they exist; new skills must be created before being referenced.

## Conventions

- Skills write their products to `.pome/nursery/<需求简称>/` (e.g. `orchard.md`, `cultivation.md`). `nursery/` holds the currently-in-progress outputs. This is a working-output directory, not source.
- SKILL.md is written in Chinese and follows the `pome-seed` structure: frontmatter, then `# <name>`, then 输入 / 规则 / 阶段 / 产物结构 / 执行流程 sections as applicable.
- There is no build, test, or lint tooling in this repo.
