# Scouting Lab

Scouting Lab is a backend football analytics platform for identifying statistically similar players using real-world performance data.

The application is built with Python, FastAPI, PostgreSQL and SQLAlchemy. Player data is collected from API-Football, stored in a relational database and exposed through a REST API.

## How it works

- Select a player: The user selects a player to use as the reference for the comparison. 
- Apply filters: The user can optionally filter the comparison by league and/or position. 
- Choose k: The user specifies the number of similar players (k) to return. 
- Represent player statistics as vectors: Each player's statistical attributes are represented as a numerical vector. 
- Calculate similarity: The system calculates the Euclidean distance between the selected player's vector and each candidate player's vector. 
- Find the nearest neighbours: The players with the smallest distances are identified using K-Nearest Neighbours (KNN). 
- Return the results: The API returns the k most similar players, including their name, position, league and similarity score. 
- Similarity score: A lower Euclidean distance indicates greater statistical similarity between two players.


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
Data Importer
     |
PostgreSQL
     |
SQLAlchemy Models
     |
Similarity Engine
     |
FastAPI REST API
