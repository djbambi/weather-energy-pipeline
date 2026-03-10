# Weather Energy Pipeline

A Python data pipeline that ingests weather and energy generation data and processes it through a Bronze, Silver, and Gold architecture.

The pipeline is designed to demonstrate production-grade Python practices, including:

- Typed domain models
- Repository-based data ingestion
- Configuration validation using Pydantic
- Prefect orchestration
- AWS S3 data lake storage
- Automated linting, formatting, and testing

## Architecture (in progress)

The pipeline will ingest data from multiple sources such as APIs, CSV files, and databases.

Data will flow through the following layers:

- **Bronze** – raw source data stored in S3
- **Silver** – cleaned and standardised datasets
- **Gold** – analytical tables (facts and dimensions)

## Development

The project uses modern Python tooling:

- `uv` for dependency management
- `ruff` for linting and formatting
- `mypy` for static typing
- `pytest` for testing
- `pre-commit` for automated checks

## Best Practices & Tasks Checklist

This checklist tracks best practices and tasks adapted from the original airflow_dag_data_pipeline project, ensuring lessons learned and improvements are applied here:

### API & Data Source
- [ ] Modularize API client so endpoints are easy to switch
- [ ] Optionally add FastAPI endpoint to serve pipeline results

### Infrastructure & DevOps
- [ ] Enforce dependency locking in CI (`uv sync --dev --frozen`)
- [ ] Optionally add `infra/` directory for infrastructure as code

### Architecture & Refactoring
- [ ] Add helpers for API request parameter construction
- [ ] Save output files with date-based filenames
- [ ] Use dependency injection for config/settings (avoid import-time init)
- [ ] Separate business logic from data engineering logic in `src/`

### Error Handling & Logging
- [ ] Use Pydantic’s `HttpUrl` for endpoint validation
- [ ] User-friendly error handling for config validation
- [ ] Robust logging for exceptions and retries

### Testing
- [ ] Add tests for retry loops and API call failures
- [ ] Optimize pytest fixture scopes
- [ ] Parametrize and consolidate tests in pytest

### Tooling
- [ ] Integrate `mypy` for static typing
- [ ] Configure `ruff` and `pre-commit` for linting and formatting

---

*This checklist is a guide for implementing modern Python best practices and continuous improvement in this project.*
