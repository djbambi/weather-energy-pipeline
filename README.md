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

# Project Plan: Weather-Energy-Pipeline

This plan lays out the roadmap for building a production-grade, medallion-architecture pipeline for weather and energy data, taking inspiration from the best-practices checklist of the original airflow_dag_data_pipeline project. Tasks already partially or fully implemented are marked, new steps are added, and optional learning extensions are included.

---

## Checklist (Status in Brackets)

### API & Data Source
- [x] Modularize API client so endpoints are easy to switch *(clients & repositories exist, extend for more APIs)*
- [ ] Optionally add FastAPI endpoint to serve pipeline results

### Infrastructure & DevOps
- [x] Enforce dependency locking in CI (`uv sync --dev --frozen`) *(check CI; uv.lock in repo)*
- [ ] Optionally add `infra/` directory for infrastructure as code

### Architecture & Refactoring
- [x] Add helpers for API request parameter construction *(present, extend as needed)*
- [x] Save output files with date-based filenames *(bronze partitioning implemented, review for silver/gold)*
- [x] Use dependency injection for config/settings (avoid import-time init) *(get_settings pattern used)*
- [x] Separate business logic from data engineering logic in `src/` *(modular src layout)*

### Error Handling & Logging
- [ ] Use Pydantic’s `HttpUrl` for endpoint validation *(confirm config usage)*
- [ ] User-friendly error handling for config validation
- [ ] Robust logging for exceptions and retries

### Testing
- [ ] Add tests for retry loops and API call failures
- [ ] Optimize pytest fixture scopes
- [ ] Parametrize and consolidate tests in pytest

### Tooling
- [x] Integrate `mypy` for static typing
- [x] Configure `ruff` and `pre-commit` for linting and formatting

---

## Immediate Next Steps

1. **Expand API Coverage**
   - Add new API clients (energy/weather sources)
   - Confirm API parameter helper abstraction is consistent

2. **Build Silver Layer**
   - Implement data cleaning and schema standardization
   - Store cleaned data in S3 (silver layer), ensure partitioning and proper file naming

3. **Build Gold Layer**
   - Define fact and dimension models (star schema); materialize gold tables
   - Store analytical outputs in S3 (gold layer)

4. **Orchestrate with Prefect**
   - Create Prefect flows for ingestion, cleaning, modeling

5. **Error Handling & Logging**
   - Use Pydantic's `HttpUrl` in config models
   - Provide clear error messages for config issues
   - Add logging for all pipeline failures, exceptions, and retries

6. **Testing**
   - Add pytest tests for retry mechanisms and edge cases
   - Review and optimize fixture scopes
   - Parametrize/merge repetitive tests

7. **Optional Extensions**
   - Add FastAPI endpoints for serving results
   - Add `infra/` for S3 setup, cloud provisioning scripts
   - Develop dashboards/notebooks for data analysis

---

## How to Use This Plan

- Track progress by marking tasks as complete
- Use the checklist for self-assessment and best practice
- Open GitHub Issues for any actionable item you wish to discuss or further document
- Expand this file as you learn, iterate, and build new pipeline features

---

*For checklist summary and quick reference, see the README. For detailed rationale, ongoing work, and implementation notes, use this document!*
