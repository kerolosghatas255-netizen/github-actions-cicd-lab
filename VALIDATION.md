# Validation Notes

## Final healthy state

Staging and production were both running the same release:

```text
Staging
commit: 7222277
version: ci-7
environment: staging
port: 8081

Production
commit: 7222277
version: ci-7
environment: production
port: 8082
```

Both containers reported healthy.

## Rollback test

A controlled production failure was introduced by using an incorrect internal port mapping.

The new release reached staging:

```text
commit: 2b68bce
version: ci-6
environment: staging
```

Production failed its health check.

The rollback step restored:

```text
commit: 9c16a1f
version: ci-5
environment: production
```

The workflow log showed:

```text
ROLLBACK SUCCESSFUL
```

The failed release remained marked as failed while the previous production image was restored.

## GitHub environment gate

The `production` environment was configured with:

- required reviewer approval
- `main` as the allowed deployment branch
- administrator bypass disabled

The workflow stopped at the production job until the deployment was manually approved.

## Registry

The tested image was published to GHCR with SHA-based tags such as:

```text
ghcr.io/kerolosghatas255-netizen/github-actions-cicd-lab:sha-<short-sha>
```

The SHA tag was used by staging and production deployments.
