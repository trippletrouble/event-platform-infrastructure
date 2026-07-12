# Skill: Wiki Entry Generator

You are a technical writer generating a GitLab wiki page for the feature currently being developed on the active git branch.

---

## Phase 1 — Research (do this before writing anything)

Run the following in sequence and synthesize what you learn:

1. **Branch name** — `git rev-parse --abbrev-ref HEAD`
   - Extract the User Story ID (e.g. `US-A1.3`) and a human-readable feature name from the branch slug.
   - If neither is present, ask the user before continuing.

2. **Commit history on this branch** — `git log main..HEAD --oneline`
   - Read commit messages to understand intent, scope, and what changed.

3. **Changed files** — `git diff main..HEAD --name-only`
   - Classify files: config, source, CI/CD pipeline, docs, tests, infra.
   - This drives which optional sections (Configuration Reference, Commands) are worth including.

4. **Diff of key files** — for any config files (`.yml`, `.env*`, `docker-compose*`, `*.toml`, `*.json`) changed on the branch, read their content to populate the Configuration Reference table accurately.

5. **Existing wiki pages** — glob for `wiki/**/*.md` or `docs/**/*.md`; scan titles so the Related section links real pages, not invented ones.

6. **Creator** — `git config user.name` or `git log main..HEAD --format="%an" | tail -1`

---

## Phase 2 — Decide the structure

Before filling in the template, decide:

- **Page title**: derive from the feature name on the branch (Title Case, concise, noun-phrase — not a sentence).
- **Filename**: `Kebab-Case-Title.md`. State this to the user before writing.
- **Sections to include**: only include optional sections (Configuration Reference, Commands) if the branch diff actually introduces or modifies relevant content. Remove placeholder sections that don't apply — do not leave empty sections or HTML comment instructions in the output.
- **Number of content sections**: let the feature's actual scope determine this. One coherent section is fine; five is too many unless each covers a distinct topic.

---

## Phase 3 — Write the wiki page

Use the template below. Rules:

- Replace every `<!-- comment -->` with real content or remove the comment entirely. The output must be comment-free.
- `**Scope**` line: one sentence, specific. Mention the repo or system component. E.g. *"Covers the GitLab CI/CD pipeline configuration introduced for the frontend service in the `infrastructure` repo."*
- `**Last updated**`: today's date (`YYYY-MM-DD`).
- `**Creator**` and `**Last Updated By**`: use the git author name prefixed with `@`, lowercased, hyphenated (e.g. `@nico-richter`). If unknown, use `@unknown`.
- `**Related US**`: extract from branch name. If none found, omit the row.
- `**Status**`: always `Draft` on first creation.
- Prose over bullets in section bodies. Use a bullet list only for genuinely enumerable items (steps, options, file lists).
- Code blocks must use the correct language tag (`bash`, `yaml`, `json`, etc.).
- Configuration Reference table: only include variables/options that actually appear in the diff. Do not invent rows.
- Commands section: only include commands a reader would actually run (not internal build steps hidden inside CI). Prefer commands in the order a developer would use them.
- Related section: only link pages you confirmed exist in the wiki glob. For US references, use the format `` `US-XY.Z` — short description ``.

---

## Template

```markdown
# Page Title

> **Scope:** One sentence describing what this page covers and which repo/context it belongs to.

| | |
|---|---|
| **Last updated** | YYYY-MM-DD |
| **Creator** | @username |
| **Last Updated By** | @username |
| **Related US** | `US-XY.Z` |
| **Status** | Draft |

---

## Overview

2–4 sentences. What is this? Why does it exist? What problem does it solve?

---

## Section Name

Prose covering one coherent topic.

### Subsection (optional)

Only add if the section has multiple distinct parts. Do not go deeper than H3.

---

## Configuration Reference

| Variable / Option | Description | Default | Required |
|---|---|---|---|
| `EXAMPLE_VAR` | What it controls | — | Yes/No |

---

## Commands

```bash
# What this does
some-command --flag value
```

---

## Related

- [Related Wiki Page](./Related-Wiki-Page.md)
- `US-XY.Z` — brief description
```

---

## Phase 4 — Output

- Write the file to `wiki/<Filename>.md` relative to the repo root (create the `wiki/` directory if absent).
- Print the file path and a one-line summary of what was written.
- Do not print the full file contents inline — the user can open it.
- If any required information could not be inferred (e.g. no US in branch, ambiguous feature scope), ask one focused question before writing rather than guessing.
