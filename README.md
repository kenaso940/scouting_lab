# Scouting Lab

Scouting Lab is a backend football analytics platform for identifying statistically similar players using real-world performance data.

The application is built with Python, FastAPI, PostgreSQL and SQLAlchemy. Player data is collected from API-Football, stored in a relational database and exposed through a REST API.

The similarity engine compares players using statistical feature vectors and weighted distance calculations, allowing different attributes to have different importance depending on player position.

## Features

- REST API built with FastAPI
- PostgreSQL database with SQLAlchemy ORM
- Database migrations managed with Alembic
- Automated player and statistics ingestion from API-Football
- Player similarity search
- Position and league filtering
- Configurable top-K results
- Position-specific similarity weighting
- Unit and API testing with Pytest
- Continuous integration with GitHub Actions
- Automated PostgreSQL setup and migration testing in CI

## Tech Stack

**Backend**
- Python
- FastAPI
- SQLAlchemy
- Pydantic

**Database**
- PostgreSQL
- Alembic

**Data Integration**
- API-Football
- Requests

**Testing and CI**
- Pytest
- FastAPI TestClient
- GitHub Actions

## Architecture


API-Football
     |
     v
Data Importer
     |
     v
PostgreSQL
     |
     v
SQLAlchemy Models
     |
     v
Similarity Engine
     |
     v
FastAPI REST API
