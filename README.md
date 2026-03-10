# Weather Energy Pipeline

A Python data pipeline that ingests weather data from the OpenWeather API and stores raw payloads in an S3-based Bronze layer. The project is the successor to [airflow_dag_data_pipeline](https://github.com/djbambi/airflow_dag_data_pipeline), rebuilt from scratch with clean architecture and modern Python tooling.

> **Current status:** The Bronze (raw ingestion) layer is working. Silver, Gold, orchestration, and additional data sources are planned.

## What's implemented

- **Bronze ingestion** — OpenWeather day-summary data fetched via a typed API client and persisted to S3 with date-partitioned keys (`bronze/{dataset}/{source}/year=YYYY/month=MM/day=DD/payload.json`)
- **Clean architecture** — Protocol-based dependency injection, ABC contracts for repositories and storage, frozen Pydantic settings with lazy `@lru_cache` initialisation
- **Immutable domain models** — `FetchWindow` and `RawPayload` as frozen dataclasses with validation
- **Adapter pattern** — `Boto3S3ClientAdapter` wraps the boto3 client behind a `SupportsS3PutObject` protocol so storage is testable without AWS
- **Test doubles** — `DummySession` and `DummyS3Client` implement the Protocols for isolated unit tests

## Project structure

```
src/weather_energy_pipeline/
├── clients/          # API clients (OpenWeather)
│   └── openweather.py
├── config/           # Pydantic settings + cached dependency provider
│   ├── settings.py
│   └── dependencies.py
├── models/           # Domain value objects
│   ├── fetch_window.py
│   └── raw_payload.py
├── repositories/     # Data-source abstractions (ABC → concrete)
│   ├── base.py
│   └── openweather.py
├── storage/          # Persistence abstractions (ABC → S3)
│   ├── base.py
│   └── s3.py
└── pipeline/         # Entry-point orchestration
    └── run_ingestion.py
```

## Development

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/) for dependency management

### Setup

```bash
uv sync --dev          # install all dependencies (including dev)
cp .env.example .env   # add your OPENWEATHER_API_KEY and BRONZE_BUCKET_NAME
```

### Common commands

| Command | What it does |
|---------|-------------|
| `make test` | Run pytest |
| `make lint` | Ruff lint check |
| `make format` | Ruff auto-format |
| `make type` | `ty` type check on `src/` |
| `make check` | All static checks (lint + format + type) |
| `make fix` | Auto-fix ruff issues |
| `make pre-commit` | Run all pre-commit hooks |

### Tooling

| Tool | Purpose |
|------|---------|
| **uv** | Dependency management and lockfile (`uv.lock`) |
| **ruff** | Linting (E, F, W, I, B, UP) and formatting |
| **ty** | Type checking (Astral's type checker) |
| **pytest** | Testing with coverage support |
| **pre-commit** | ruff + standard hooks (trailing whitespace, YAML, TOML) |

---

## Original issues tracker

This project carries forward 16 open issues from the original [airflow_dag_data_pipeline](https://github.com/djbambi/airflow_dag_data_pipeline). The tables below track each one against the current codebase.

### Resolved

| Original | Issue | How it's addressed |
|----------|-------|--------------------|
| [#10](https://github.com/djbambi/airflow_dag_data_pipeline/issues/10) | Extract request param construction into client helper | `OpenWeatherApiClient.fetch_day_summary()` builds params internally |
| [#14](https://github.com/djbambi/airflow_dag_data_pipeline/issues/14) | Date-based filenames | `S3RawStorage._build_key()` generates `year=YYYY/month=MM/day=DD/` paths |
| [#36](https://github.com/djbambi/airflow_dag_data_pipeline/issues/36) | Remove import-time Settings init | `get_settings()` with `@lru_cache` — lazy, never at import time |
| [#53](https://github.com/djbambi/airflow_dag_data_pipeline/issues/53) | Switch from mypy to ty | `ty` configured in `pyproject.toml`, Makefile target runs `ty check` |
| [#55](https://github.com/djbambi/airflow_dag_data_pipeline/issues/55) | Separate business logic from data engineering | Layered `src/` layout: clients → repositories → storage → pipeline |

### Open — next up

| Original | Issue | What's needed |
|----------|-------|---------------|
| [#19](https://github.com/djbambi/airflow_dag_data_pipeline/issues/19) | Restore `HttpUrl` for base URL | Change `openweather_base_url: str` to `HttpUrl` in `settings.py` |
| [#29](https://github.com/djbambi/airflow_dag_data_pipeline/issues/29) | User-friendly error for missing env vars | Catch `ValidationError` in `main()`, print clean message, exit 1 |
| [#39](https://github.com/djbambi/airflow_dag_data_pipeline/issues/39) | Log HTTP status on retry | Implement retry logic in the API client using the existing retry settings, add `logging` |
| [#34](https://github.com/djbambi/airflow_dag_data_pipeline/issues/34) | Retry loop tests | Blocked on #39 — once retries exist, add tests for 503→200 scenarios |
| [#18](https://github.com/djbambi/airflow_dag_data_pipeline/issues/18) | Frozen/locked installs in CI | Create a GitHub Actions workflow using `uv sync --dev --frozen` |
| [#40](https://github.com/djbambi/airflow_dag_data_pipeline/issues/40) | Review fixture scopes | Audit fixtures for `module`/`session` scope opportunities |
| [#41](https://github.com/djbambi/airflow_dag_data_pipeline/issues/41) | Consolidate tests with parametrize | Merge similar test cases using `@pytest.mark.parametrize` |

### Open — optional / future

| Original | Issue | Notes |
|----------|-------|-------|
| [#51](https://github.com/djbambi/airflow_dag_data_pipeline/issues/51) | Switch to OpenMeteo API | Add as a second data source alongside OpenWeather |
| [#52](https://github.com/djbambi/airflow_dag_data_pipeline/issues/52) | FastAPI endpoint | Serve pipeline results over HTTP |
| [#54](https://github.com/djbambi/airflow_dag_data_pipeline/issues/54) | `infra/` directory for IaC | Pulumi or Terraform for S3 bucket provisioning |

### Dropped

| Original | Issue | Reason |
|----------|-------|--------|
| [#12](https://github.com/djbambi/airflow_dag_data_pipeline/issues/12) | PySpark + Docker | Airflow/Spark-specific; not relevant to this architecture |

---

## Roadmap

Work is sequenced so each phase builds on the previous one and delivers a working increment.

### Phase 1 — Harden the Bronze layer

The ingestion path works but lacks resilience and observability.

1. **Add structured logging** — configure Python `logging` across all modules; log API calls, S3 writes, and errors
2. **Implement retry logic** — use the existing retry settings (`max_retry_attempts`, `retry_backoff_multiplier`, etc.) to add exponential backoff in `OpenWeatherApiClient` (#39)
3. **Restore `HttpUrl` validation** — change `openweather_base_url` from `str` to Pydantic `HttpUrl` (#19)
4. **User-friendly config errors** — catch `ValidationError` at the entry point, print a clean message listing each missing/invalid variable (#29)
5. **Retry tests** — pytest cases that simulate transient failures (503 → 200) and verify the retry loop (#34)
6. **Test improvements** — review fixture scopes (#40), add `@pytest.mark.parametrize` where tests repeat (#41)

### Phase 2 — CI and reproducibility

7. **GitHub Actions workflow** — lint, type-check, and test on push/PR; use `uv sync --dev --frozen` to enforce lockfile (#18)
8. **Coverage gate** — add `pytest-cov` threshold to CI so coverage doesn't regress

### Phase 3 — Silver layer

9. **Define Silver models** — Pydantic models for cleaned/standardised weather records
10. **Implement Silver transformation** — read Bronze JSON, validate, clean, and write to `silver/` partition in S3
11. **Silver tests** — unit tests for transformation logic and edge cases

### Phase 4 — Additional data sources

12. **OpenMeteo client** — add a second API client and repository following the same Protocol pattern (#51)
13. **Energy data source** — add an energy generation data client (API or CSV)

### Phase 5 — Gold layer

14. **Define fact/dimension models** — star-schema tables for analytical queries
15. **Implement Gold aggregation** — read Silver data, compute metrics, write to `gold/` in S3
16. **Gold tests**

### Phase 6 — Orchestration with Prefect

17. **Add Prefect dependency** and create flows/tasks wrapping each pipeline stage
18. **Schedule flows** — daily ingestion, transformation, aggregation
19. **Prefect dashboard** — configure for visibility into runs, retries, and failures

### Optional extensions

- **FastAPI** — serve Gold layer results over HTTP (#52)
- **`infra/` directory** — Pulumi/Terraform for S3 and IAM provisioning (#54)
- **Dashboards** — Jupyter notebooks or Streamlit for exploring Gold data
