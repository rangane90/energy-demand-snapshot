# Energy Demand Snapshot

[![CI](https://github.com/rangane90/energy-demand-snapshot/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rangane90/energy-demand-snapshot/actions/workflows/ci.yml)

A small Python API that summarizes synthetic hourly electricity demand. I built it to connect my interest in energy forecasting with the software delivery practices that make an engineering tool repeatable to build and test.

The API returns the sample count, average demand, and peak demand in megawatts. The fixture contains eight fictional readings and is included with the app.

## Run locally

From this directory with Python 3.12 installed, run:

```powershell
python -B -m unittest -v
python -B app.py
```

Open [the health endpoint](http://127.0.0.1:8080/health) and [the demand summary](http://127.0.0.1:8080/summary), or run this in a second terminal:

```powershell
curl.exe http://127.0.0.1:8080/summary
```

```json
{"data_source": "synthetic", "samples": 8, "average_mw": 490, "peak_mw": 720}
```

## Run in Docker

```powershell
docker build -t energy-demand-snapshot:local .
docker run --rm -p 127.0.0.1:8080:8080 energy-demand-snapshot:local
```

The container runs as a non-root user. The Python app uses only the standard library.

## Continuous integration

GitHub Actions runs on pushes to `main` and pull requests targeting `main`. The workflow runs the HTTP tests, builds a Docker image labeled with the commit SHA, starts it, and checks both endpoints. The smoke test checks the returned summary against the included fixture.

## Jenkins pipeline

The [verified Jenkins run](https://github.com/rangane90/energy-demand-snapshot/actions/runs/42780648885) ran all three HTTP tests, built the commit-tagged Docker image, and smoke-tested the container. The run includes the Jenkins console output and a downloadable log retained for 30 days.

To repeat the check, run [Jenkins verification](https://github.com/rangane90/energy-demand-snapshot/actions/workflows/jenkins.yml) from the Actions tab. It starts Jenkins on a temporary Linux runner.

Use a Pipeline job configured from a Git repository with this Jenkinsfile. The agent needs the `docker` label, Git, Python 3.12, and access to a Linux Docker engine.

1. Run HTTP tests for the health endpoint, summary, and unknown routes.
2. Build an image tagged and labeled with the full Git commit SHA.
3. Start that image, check the summary endpoint, and remove the test container when the step exits.

The Jenkins image stays on the agent. This demo uses a local fixture and a local container to keep the release process easy to reproduce.
