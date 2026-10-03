# GitHub Actions CI/CD Lab

I built this project to practice a complete CI/CD release workflow using GitHub Actions and Docker.

The application itself is intentionally small. The main focus of the project is the delivery pipeline: testing code, building a container image, scanning it, publishing it to a registry, deploying to staging, validating the deployment, and later promoting the same image to production with rollback support.

Current application endpoints:

- `/` - basic application status
- `/health` - deployment health check
- `/version` - shows application version, commit, and environment

The project will use:

- GitHub Actions
- Docker
- GitHub Container Registry
- Staging and production environments
- Automated health checks
- Release versioning
- Production deployment gates
- Rollback testing
