# Project decisions

| Interface | Value | Brief reference |
|---|---|---|
| Application port | 3000 | n/a |
| Health check | GET /health (JSON: status, commit, environment, build_time) | 1.3, 1.4 |
| Monitoring metrics | GET /metrics (Prometheus format, includes HTTP latency) | 3.5 |
| Environment variables | APP_ENV, GIT_COMMIT, BUILD_TIME, DB_PATH | 1.3 |
| Database | SQLite, file stored in a Docker volume | 1.3 |
| Image name | build-status-dashboard (GHCR: ghcr.io/mangeloguy/build-status-dashboard) | 1.1, Fig. 1 |
| Deployment command | docker compose pull && docker compose up -d | 5.1 |
| CI trigger | Push or merge to main | 5.1 |
| Secrets | SSH key, AWS credentials, registry token, kept in GitHub Secrets only | n/a |

## Open points (team to confirm)

- Registry: the brief does not name one. GHCR is proposed.
- Image tags: build once, tag with the short commit SHA, and only move `latest` after staging passes, so production never pulls an untested image (1.1, Fig. 1).