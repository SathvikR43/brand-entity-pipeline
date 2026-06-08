# Brand Entity Pipeline

A production-style data engineering project that ingests brand/company data from public sources, resolves duplicate entities, validates data quality, and serves clean structured data via a REST API.

Built to demonstrate end-to-end data engineering ownership: ingestion → entity resolution → storage → data quality → API layer.

---

## Architecture

Wikidata API
↓
Ingestion (Python)
↓
PostgreSQL (brands, aliases, pipeline_runs)
↓
Entity Resolution (fuzzy matching + confidence scoring)
↓
Data Quality Checks (schema validation, freshness SLAs)
↓
Flask REST API

## Tech Stack

- **Language:** Python, SQL
- **Database:** PostgreSQL
- **Pipeline:** Custom ETL with entity resolution
- **API:** Flask
- **Data Source:** Wikidata (public API)
---

## Project Structure

brand-entity-pipeline/
├── ingestion/          # Fetch brand data from Wikidata API
├── resolution/         # Fuzzy entity deduplication + confidence scoring
├── database/           # PostgreSQL schema + data loader
├── quality/            # Schema validation, freshness checks, pipeline logging
├── api/                # Flask REST API
├── config/             # Environment settings
├── run_pipeline.py     # Master script — runs full pipeline end to end
├── requirements.txt
└── .env                # DB credentials (not committed)


---

## Setup

**1. Clone the repo and create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up PostgreSQL and create the database**
```bash
psql -U postgres -p 5433
CREATE DATABASE brand_pipeline;
\c brand_pipeline
```

Then run the schema SQL from `database/schema.sql`.

**4. Configure environment variables**

Create a `.env` file:

DB_HOST=localhost
DB_PORT=5433
DB_NAME=brand_pipeline
DB_USER=postgres
DB_PASSWORD=your_password


**5. Run the pipeline**
```bash
python run_pipeline.py
```

**6. Start the API**
```bash
python api/app.py
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/brands` | GET | List all brands (top 50 by confidence) |
| `/brands?name=Nike` | GET | Search brands by name |
| `/brands/<id>/aliases` | GET | Get all aliases for a brand |
| `/quality` | GET | View pipeline run history |
| `/health` | GET | Health check |

---

## Key Features

- **Entity Resolution** — fuzzy matching with configurable similarity threshold (default 85%) to detect and merge duplicate brand records
- **Confidence Scoring** — each brand gets a confidence score based on match quality
- **Alias Tracking** — duplicate names stored as aliases, preserving lineage
- **Data Quality Monitoring** — tracks missing fields, flags low-confidence records, logs every pipeline run
- **Pipeline Logging** — every run recorded in `pipeline_runs` table with record counts and status


