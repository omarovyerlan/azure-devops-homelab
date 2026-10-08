# Azure DevOps Home Lab

![CI](https://github.com/omarovyerlan/azure-devops-homelab/actions/workflows/ci.yml/badge.svg)

A hands-on DevOps project. A small status web app is containerized with Docker, and will be deployed to Azure using Terraform, Ansible and a GitHub Actions CI/CD pipeline.

## Roadmap

| Stage | What | Status |
|---|---|---|
| 1 | Containerize the app with Docker | ✅ Done |
| 2 | CI: GitHub Actions runs tests and builds the image on every push | ✅ Done |
| 3 | Terraform: create the Azure network, firewall rules and Linux VM | ⏳ Next |
| 4 | Ansible: harden the VM and install Docker | ⏳ |
| 5 | CD: deploy the new container automatically | ⏳ |
| 6 | Monitoring with Prometheus and Grafana | ⏳ |

## Stage 1: the app

A Python (Flask) status dashboard with three endpoints:

| Endpoint | Purpose |
|---|---|
| `/` | Status page (hostname, version, uptime) |
| `/health` | Health check used by Docker, load balancers and monitoring |
| `/api/info` | The same info as JSON |

## Docker practices used

- **Small official base image** (`python:3.13-slim`)
- **Layer caching:** dependencies install before the code is copied, so rebuilds are fast
- **Runs as a non-root user** (`appuser`), which limits damage if the app is compromised
- **`HEALTHCHECK`** so Docker knows when the container is unhealthy
- **Production web server** (gunicorn) instead of Flask's development server
- **`.dockerignore`** keeps tests and cache files out of the image
- **Version passed in at build time** (`APP_VERSION`), ready for CI tagging
- **Pinned dependency versions** for repeatable builds

## Run it

You need [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine.

```bash
# Build and start
docker compose up -d --build

# Open the app
open http://localhost:8080        # or just visit it in a browser

# Check health and logs
curl http://localhost:8080/health
docker ps                          # STATUS should say "(healthy)" after ~30s
docker logs homelab-status

# Prove it runs as non-root
docker exec homelab-status whoami  # -> appuser

# Stop and remove
docker compose down
```

Without Compose:

```bash
docker build -t homelab-status:0.1.0 --build-arg APP_VERSION=0.1.0 ./app
docker run -d -p 8080:8080 --name homelab-status homelab-status:0.1.0
```

## Run the tests

```bash
cd app
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m pytest
```

## Project structure

```
azure-devops-homelab/
├── app/
│   ├── app.py               # Flask application
│   ├── templates/index.html # Status page
│   ├── tests/test_app.py    # Unit tests (pytest)
│   ├── requirements.txt     # Runtime dependencies
│   ├── requirements-dev.txt # + test dependencies
│   ├── Dockerfile
│   └── .dockerignore
├── docker-compose.yml
└── README.md
```

## What I learned

*(Fill this in as you go. Interviewers often ask about it, e.g. why layer order matters in a Dockerfile, or why containers should not run as root.)*
