# Build Status Dashboard

SWE40006 Project, Group 02. A containerised web app that shows its own deployment state (commit, build time, environment, health, deploy history), used to demonstrate a four-stage CI/CD pipeline.

## Run locally

Requires Docker.

    docker build -t build-status-dashboard:latest --build-arg GIT_COMMIT=local --build-arg BUILD_TIME=local .
    docker run --rm -p 3000:3000 build-status-dashboard:latest

Then check:

    curl localhost:3000/health
    curl localhost:3000/metrics

## Layout

- `app/`: application code
- `tests/`: unit, integration and end-to-end tests
- `docker/`: compose files for staging and production
- `.github/workflows/`: CI/CD pipeline

See `DECISIONS.md` for the agreed interfaces (port, endpoints, env vars, image name).