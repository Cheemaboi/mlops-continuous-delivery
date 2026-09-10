# Implementation Evidence

This record distinguishes verified results from configuration that requires external deployment infrastructure.

## Verified locally

- `pytest`: 4 tests passed for `/`, `/health`, valid `/predict`, and invalid prediction input.
- Docker image: built locally from `python:3.12-slim`.
- Docker run: `/health` returned HTTP 200 with `application_version`, `model_version`, `git_commit`, and `status: healthy`.
- Docker prediction: `POST /predict` with `{"value": 5}` returned prediction `10.0`.

## GitHub verification

- Pull request CI passed for PRs #1 through #4. CI contains tests only; it has no package or deployment permission.
- GitHub Environments `staging` and `production` exist.
- The `v1.2.0` release workflow tested and built/published the versioned and `latest` GHCR image successfully.
- `v1.2.0` staging failed because no staging host, user, or SSH key secret has been configured. The health gate and production job were consequently not reached.

## Pending external evidence

The following cannot be truthfully recorded until deployment credentials and a reachable Docker host are supplied:

- successful staging deployment and health gate;
- production approval event and deployment;
- a live rollback health response from `1.3.0` to `1.2.0`.

Do not move existing tags. Capture the Actions run, GHCR package listing, staging health response, approval screen, production deployment, and rollback health response after real deployment.

## Release traceability

The CD build determines the real release revision with `git rev-parse --short HEAD` and supplies it as Docker build metadata. The application exposes that value at `/health` via `git_commit`.
