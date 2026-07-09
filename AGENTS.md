# Nicolas Richter - AGENTS.md
## 0. Call me by Name

In **every** answer always call me by name "Nico" in the beginning

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.


## Issue Tracking

Whenever you encounter a bug, blocker, or unexpected behavior — **before continuing work** — add an entry to `/docs/issues.md` in the project root.

Use this format:

```markdown
### [ISSUE-###] Title

- **Status:** Open | In Progress | Resolved
- **Severity:** Critical | High | Medium | Low
- **Reported:** YYYY-MM-DD
- **Resolved:** YYYY-MM-DD _(leave blank if unresolved)_
- **Component:** e.g. API / Auth / DB / Frontend / Infrastructure

**Description:**
What is broken, what is the unexpected behavior, and where does it occur?

**Steps to Reproduce:**
1. ...
2. ...

**Fix:**
Root cause and resolution. Include code snippets, config changes, or commands as needed.

- [ ] Resolved
```

**Rules:**
- Assign the next sequential `ISSUE-###` ID.
- Do not continue implementing past a blocker without logging it first.
- When you fix an issue yourself: check the checkbox, set `Status: Resolved`, and fill in `Resolved` date.
- Do not delete resolved entries — keep them for audit.
- Severity guide:
    - **Critical** — system won't start, data loss, security hole
    - **High** — core feature broken, no workaround
    - **Medium** — degraded behavior, workaround exists
    - **Low** — cosmetic, minor inconsistency

## Graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).


## Project-Specific Guidelines

### Tech-Stack
- NestJS
- TypeScript
- Prisma ORM
- PostgreSQL

### Tests
- Test coverage > 90%

### Database Dependency Inversion (DIP)
- High-level business services (e.g., `EventsService`) MUST NOT import or inject `PrismaService` or `PrismaClient` directly.
- Always inject the abstract repository class token from `src/repositories/interfaces/` (e.g., `UserRepository`, `EventInterface`).
- Implement concrete database access methods under `src/repositories/prisma/` and verify they are registered in the global `RepositoriesModule`.

### Database Schema Changes
- If you modify `schema.prisma`, immediately run:
  1. `npx prisma generate` to rebuild the local Prisma Client.
  2. `npx prisma migrate dev --name <migration_name>` (or the corresponding dockerized command) to apply schema changes to PostgreSQL.
- Ensure seed scripts (`prisma/seed.ts`) are updated to include required new properties/relations.




# Naila Jochner - AGENTS.md
0. Call me by Name
   In every answer always call me by name "Naila" in the beginning

1. Think Before Coding
   Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

State your assumptions explicitly. If uncertain, ask.
If multiple interpretations exist, present them - don't pick silently.
If a simpler approach exists, say so. Push back when warranted.
If something is unclear, stop. Name what's confusing. Ask.
2. Simplicity First
   Minimum code that solves the problem. Nothing speculative.

No features beyond what was asked.
No abstractions for single-use code.
No "flexibility" or "configurability" that wasn't requested.
No error handling for impossible scenarios.
If you write 200 lines and it could be 50, rewrite it.
Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

3. Surgical Changes
   Touch only what you must. Clean up only your own mess.

When editing existing code:

Don't "improve" adjacent code, comments, or formatting.
Don't refactor things that aren't broken.
Match existing style, even if you'd do it differently.
If you notice unrelated dead code, mention it - don't delete it.
When your changes create orphans:

Remove imports/variables/functions that YOUR changes made unused.
Don't remove pre-existing dead code unless asked.
The test: Every changed line should trace directly to the user's request.

4. Goal-Driven Execution
   Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

"Add validation" → "Write tests for invalid inputs, then make them pass"
"Fix the bug" → "Write a test that reproduces it, then make it pass"
"Refactor X" → "Ensure tests pass before and after"
For multi-step tasks, state a brief plan:

1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
   Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

Issue Tracking
Whenever you encounter a bug, blocker, or unexpected behavior — before continuing work — add an entry to /docs/issues.md in the project root.

Use this format:

### [ISSUE-###] Title

- **Status:** Open | In Progress | Resolved
- **Severity:** Critical | High | Medium | Low
- **Reported:** YYYY-MM-DD
- **Resolved:** YYYY-MM-DD _(leave blank if unresolved)_
- **Component:** e.g. API / Auth / DB / Frontend / Infrastructure

**Description:**
What is broken, what is the unexpected behavior, and where does it occur?

**Steps to Reproduce:**
1. ...
2. ...

**Fix:**
Root cause and resolution. Include code snippets, config changes, or commands as needed.

- [ ] Resolved
  Rules:

Assign the next sequential ISSUE-### ID.
Do not continue implementing past a blocker without logging it first.
When you fix an issue yourself: check the checkbox, set Status: Resolved, and fill in Resolved date.
Do not delete resolved entries — keep them for audit.
Severity guide:
Critical — system won't start, data loss, security hole
High — core feature broken, no workaround
Medium — degraded behavior, workaround exists
Low — cosmetic, minor inconsistency
Project-Specific Guidelines
Tech-Stack
NestJS
NextJS with React
TypeScript
Prisma ORM
PostgreSQL
Tests
Test coverage > 90%
Database Dependency Inversion (DIP)
High-level business services (e.g., EventsService) MUST NOT import or inject PrismaService or PrismaClient directly.
Always inject the abstract repository class token from src/repositories/interfaces/ (e.g., UserRepository, EventInterface).
Implement concrete database access methods under src/repositories/prisma/ and verify they are registered in the global RepositoriesModule.
Database Schema Changes
If you modify schema.prisma, immediately run:
npx prisma generate to rebuild the local Prisma Client.
npx prisma migrate dev --name <migration_name> (or the corresponding dockerized command) to apply schema changes to PostgreSQL.
Ensure seed scripts (prisma/seed.ts) are updated to include required new properties/relations.
