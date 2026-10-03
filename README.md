# GitHub Actions CI/CD Lab

## Overview

I built this project to practice a complete CI/CD release flow with GitHub Actions and Docker.

The application is intentionally small. The main focus is the delivery process around it: linting and tests, building one Docker image, scanning it, publishing it to GitHub Container Registry, deploying the same image to staging and production, checking the deployed version, using a production approval gate, and rolling back automatically when a production release fails.

## Application

The Flask application has three endpoints:

- `/` - basic application status
- `/health` - health check used by the pipeline
- `/version` - shows the application version, commit SHA, and environment

Example:

```json
{
  "commit": "7222277",
  "environment": "production",
  "version": "ci-7"
}
```

The version endpoint makes it easy to verify which release is actually running in each environment.

## Pipeline

```text
Push / Pull Request
        |
        v
Lint and Unit Tests
        |
        v
Docker Build
        |
        v
Container Smoke Test
        |
        v
Trivy Security Scan
        |
        v
GitHub Container Registry
        |
        v
Staging Deployment :8081
        |
        v
Health + Version Check
        |
        v
Production Approval
        |
        v
Production Deployment :8082
        |
        v
Health + Version Check
        |
        +---- failure ----> Automatic Rollback
```

## CI

The CI part runs on GitHub-hosted runners and performs:

- Ruff linting
- Pytest unit tests
- Docker image build
- container startup
- `/health` verification
- `/version` verification
- Trivy scan for critical vulnerabilities

The Docker job only starts after the lint and test job succeeds.

## Container Publishing

After the image passes the checks, the pipeline publishes it to GitHub Container Registry.

Images are tagged with the short commit SHA, for example:

```text
ghcr.io/kerolosghatas255-netizen/github-actions-cicd-lab:sha-7222277
```

The pipeline also updates the `latest` tag.

Using the SHA tag makes it possible to deploy and roll back to an exact release.

## Self-hosted Runner

Deployments run on a self-hosted GitHub Actions runner installed as a systemd service on an Ubuntu VM.

Runner labels include:

```text
self-hosted
Linux
X64
staging
cicd-lab
```

The runner has Docker access and is used only for deployment jobs from `main`.

## Staging

Staging is deployed automatically after the image is published.

The staging container runs on port `8081`.

The deployment job:

1. pulls the image tagged with the current commit SHA
2. replaces the previous staging container
3. waits for `/health`
4. verifies the commit in `/version`
5. verifies that the environment is `staging`

## Production

Production runs on port `8082`.

The production job depends on a successful staging deployment.

It also uses a GitHub Environment named `production` with:

- required reviewer approval
- deployments restricted to `main`
- administrator bypass disabled

This creates a manual gate between staging and production.

## Build Once, Deploy the Same Image

Staging and production use the same image tag.

After the final recovery run both environments were running:

```text
commit: 7222277
version: ci-7
```

The only difference was the runtime environment variable:

```text
staging    -> APP_ENV=staging
production -> APP_ENV=production
```

The image was not rebuilt for production.

## Automatic Rollback

Before replacing the production container, the pipeline records the image currently running in production.

If the new production deployment fails its health check, the rollback step:

1. removes the failed container
2. starts the previous production image
3. waits for the previous version to become healthy
4. prints the restored version

I tested the rollback with a controlled failure by mapping production to the wrong internal port.

The new release reached staging successfully:

```text
commit: 2b68bce
version: ci-6
environment: staging
```

The production health check failed and the workflow restored the previous image:

```text
commit: 9c16a1f
version: ci-5
environment: production
```

The rollback log reported:

```text
ROLLBACK SUCCESSFUL
```

The workflow run stayed failed, which is intentional. The release failed even though the previous production version was restored successfully.

After the rollback test, the failure injection was reverted and a clean deployment completed successfully. Staging and production were both running:

```text
commit: 7222277
version: ci-7
```

## Pull Requests vs Main

Pull requests run validation only:

```text
lint
tests
Docker build
smoke test
security scan
```

Publishing and deployment happen only on pushes to `main`.

This keeps pull request changes away from the self-hosted deployment runner.

## Project Files

```text
github-actions-cicd-lab/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_app.py
├── app.py
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## Tools Used

- GitHub Actions
- Docker
- GitHub Container Registry
- GitHub Environments
- GitHub self-hosted runner
- Python / Flask
- Gunicorn
- Pytest
- Ruff
- Trivy
- systemd
- Ubuntu Linux

## What I Tested

I tested the pipeline rather than only checking the configuration.

That included:

- linting and unit tests
- Docker image build
- container health
- release metadata
- critical vulnerability scanning
- GHCR publishing
- self-hosted runner deployment
- automatic staging deployment
- production approval
- same-image promotion from staging to production
- controlled production failure
- automatic rollback
- final clean deployment after restoring the normal production configuration

The goal of the project was to understand the full release flow and what happens when a release succeeds, waits for approval, or fails after reaching production.
