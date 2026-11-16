# CloudPulse

A Python website monitoring dashboard and DevOps portfolio project. CloudPulse periodically checks multiple websites, records HTTP status and latency to SQLite, and displays a dashboard with health status, response time trends, and recent incidents.

## Features
- Multiple websites configured using `MONITOR_URLS`
- HTTP status checks, response time, and timeout/error detection
- SQLite check history and incidents
- Flask dashboard at `/`, JSON API at `/api/status`, service endpoint at `/health`
- Docker image and GitHub Actions CI for unit tests and Docker build

## Run locally (Windows PowerShell)

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open http://localhost:5000 in your browser.

Run a single monitoring check:

```powershell
.\.venv\Scripts\python.exe monitor.py
```

Run unit tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Configuration

Environment variables:

| Variable | Default | Description |
|---|---|---|
| `MONITOR_URLS` | `https://example.com,https://www.python.org` | Comma-separated sites |
| `CHECK_INTERVAL` | `60` | Seconds between checks (minimum 10) |
| `CLOUDPULSE_DB` | `cloudpulse.db` | SQLite database path |
| `PORT` | `5000` | Dashboard port |

Example in PowerShell (before starting the app):

```powershell
$env:MONITOR_URLS="https://example.com,https://www.python.org"
$env:CHECK_INTERVAL="30"
.\.venv\Scripts\python.exe app.py
```

## Docker

```powershell
docker build -t cloudpulse .
docker run --rm -p 5000:5000 -e MONITOR_URLS="https://example.com,https://www.python.org" cloudpulse
```

For persistent history, mount a volume and set `CLOUDPULSE_DB` to a path in that volume.

## Architecture

`HTTP checks → Python requests → SQLite → Flask JSON API → HTML dashboard`

GitHub Actions runs unit tests and builds the Docker image on pushes and pull requests.

## Scope and limitations

This is a portfolio MVP, not a production monitoring service. Checks run in the Flask process; production deployments should use a separate worker and persistent database, authentication, rate limiting, alert delivery, and operational safeguards. The dashboard reports the last 100 checks, not total lifetime checks.

## License
MIT — see repository license file.
