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
