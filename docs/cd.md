# CD Pipeline — Handoff Document

## Project Context

- **Repo**: `gitlab.hof-university.de/events/backend`
- **Stack**: NestJS 11, TypeScript, Prisma 7, PostgreSQL, MinIO, Stripe, OIDC auth
- **Branch**: `feat/US-R3.3-hypermedia_links` (work done here, not yet merged)
- **Branching strategy**: `master` (production), `develop` (integration), feature branches via MRs
- **Docker**: Multi-stage build (`node:22-alpine`), images pushed to GitLab Container Registry
- **Proxy**: All CI jobs go through `proxy.hof-university.de:3128`

## What Was Done

### Phase 1: Dockerfile Security Fix
- **`Dockerfile`**: Removed `COPY --from=builder /app/.env ./.env` — secrets were baked into the image. Environment variables must now be injected at runtime via docker-compose `env_file` or `environment:` blocks.
- **`Dockerfile`**: Added `HEALTHCHECK` directive hitting `GET /health`.
- **`.dockerignore`** (new): Excludes `.env`, `.env.*`, `node_modules`, `dist`, `coverage`, `.git`, `*.md`, `graphify-out` from Docker build context.

### Phase 2: Health Check Endpoints
- **`src/health/health.controller.ts`** (new): Two endpoints:
  - `GET /health` — liveness probe, returns `{ status: 'ok', timestamp }`.
  - `GET /health/ready` — readiness probe, runs `SELECT 1` against PostgreSQL via PrismaService.
- **`src/health/health.module.ts`** (new): NestJS module, no imports needed since `PrismaModule` is `@Global()`.
- **`src/app.module.ts`**: Added `HealthModule` to imports array.

### Phase 3: Full CI/CD Pipeline Rewrite
- **`.gitlab-ci.yml`**: Rewritten from 4 stages to 7 stages:

| Stage | Jobs | Trigger |
|---|---|---|
| `prepare` | `install` — runs `npm ci` + `prisma generate`, caches as artifacts | MR, master, develop |
| `validate` | `lint` — uses `needs: ["install"]`, no own `npm ci` | MR, master, develop |
| `test` | `unit-tests` — uses `needs: ["install"]` | MR, master, develop |
| `build` | `build` — uses `needs: ["install"]` | master, develop |
| `docker` | `docker-build` — needs build + unit-tests | master, develop |
| `deploy-staging` | `deploy-staging` + `smoke-test-staging` | develop (automatic) |
| `deploy-production` | `deploy-production` + `smoke-test-production` + `rollback-production` | master (manual gate) |

Key design decisions:
- **`install` job** deduplicates `npm ci` + `prisma generate` across all downstream jobs via artifacts.
- **Default image** fixed from `node:25-alpine` to `node:22-alpine` (matches Dockerfile).
- **Deploy jobs** use SSH into the target server, pull the image, and run `docker compose up -d nestjs`.
- **Smoke tests** retry `GET /health/ready` up to 12 times (60s total) after each deploy.
- **Rollback job** is manual; operator sets `ROLLBACK_SHA` variable to a previous commit SHA when triggering.
- **Production deploy** requires manual approval (`when: manual`, `allow_failure: false`).

## What Still Needs To Be Done

### 1. GitLab CI/CD Variables (BLOCKING — pipeline won't deploy without these)
Configure in **GitLab > Settings > CI/CD > Variables**:

| Variable | Type | Protected | Description |
|---|---|---|---|
| `STAGING_SSH_KEY` | File | Yes | SSH private key for staging server |
| `STAGING_HOST` | Variable | Yes | Staging server hostname/IP |
| `STAGING_USER` | Variable | Yes | SSH username for staging |
| `STAGING_DEPLOY_PATH` | Variable | No | Path to docker-compose on staging (e.g. `/opt/events`) |
| `STAGING_URL` | Variable | No | Base URL for smoke tests (e.g. `https://staging.example.com`) |
| `PROD_SSH_KEY` | File | Yes | SSH private key for production server |
| `PROD_HOST` | Variable | Yes | Production server hostname/IP |
| `PROD_USER` | Variable | Yes | SSH username for production |
| `PROD_DEPLOY_PATH` | Variable | No | Path to docker-compose on production |
| `PRODUCTION_URL` | Variable | No | Base URL for smoke tests |
| `CI_POSTGRES_URL` | Variable | Yes | PostgreSQL URL for CI test runs (may already exist) |
| `CI_JWT_SECRET` | Variable | Yes | JWT secret for CI test runs (may already exist) |

**Recommendation**: Generate a dedicated ed25519 deploy key (`ssh-keygen -t ed25519 -C "gitlab-cd-deploy"`) rather than using personal keys.

### 2. Server-Side docker-compose Configuration
The deploy jobs expect the target server to have:
- Docker and docker-compose installed
- A `docker-compose.yml` at `$STAGING_DEPLOY_PATH` / `$PROD_DEPLOY_PATH` with a `nestjs` service
- The `nestjs` service must accept `BACKEND_IMAGE` as the image reference (the deploy script sets this env var)
- Environment variables (`.env` file or `environment:` block) on the server, since they are no longer baked into the image

### 3. Database Migrations (Not Yet Separated)
Currently `CMD ["npm", "run", "start:migrate:prod"]` runs `prisma migrate deploy` at container startup. This works for single-instance deployments but is risky for multi-replica. A future improvement:
- Add a dedicated `migrate` CI job before `deploy-*` that runs `prisma migrate deploy` against the target database
- Change the Dockerfile CMD to just `["node", "dist/main.js"]`

### 4. E2E Tests in CI (Not Yet Added)
The `test/jest-e2e.json` config exists but e2e tests are not run in the pipeline. To add:
- Create an `e2e-tests` job in the `test` stage with a `postgres` service
- Run on MR pipelines to catch integration issues before merge

### 5. Deployment Notifications (Not Yet Added)
Consider adding a job that posts to Slack/Teams on deploy success/failure using a webhook URL stored in CI variables.

### 6. Pre-Existing Type Errors (Unrelated)
Two test files have type errors due to a missing `imageUrl` property — these predate this work:
- `src/admin/controllers/companies.admin.controller.spec.ts:100`
- `src/repositories/interfaces/admin.interface.spec.ts:175`

## File Inventory (All Changes)

| File | Status | Purpose |
|---|---|---|
| `.gitlab-ci.yml` | Modified | Full pipeline with deploy stages |
| `Dockerfile` | Modified | Removed .env copy, added HEALTHCHECK |
| `.dockerignore` | New | Excludes secrets and unnecessary files from build context |
| `src/health/health.controller.ts` | New | Liveness + readiness endpoints |
| `src/health/health.module.ts` | New | Health module registration |
| `src/app.module.ts` | Modified | Added HealthModule import |