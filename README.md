# Unified Consent Management Platform (UCMP)

## Overview

The Unified Consent Management Platform (UCMP) is a scalable,
event-driven backend system designed to:

-   Store user consent history from multiple source systems
-   Maintain the current active consent state
-   Support auditability and regulatory compliance
-   Handle duplicate and late-arriving events
-   Scale efficiently beyond 1M+ records

The system standardizes consent updates from various platforms (Website,
CRM, Event Platform, etc.) into a canonical data model and stores them
in a normalized relational schema.

------------------------------------------------------------------------

## Architecture Summary

### Ingestion Layer

-   FastAPI (simulating API Gateway)
-   Canonical transformation logic
-   Idempotency validation

### Processing Layer

-   Deduplication using processed_events table
-   Versioning logic
-   Late-arrival handling
-   Current-state upsert logic

### Storage Layer

-   PostgreSQL (RDS in AWS / Local for simulation)
-   Immutable consent_history ledger
-   Optimized consent_current table

------------------------------------------------------------------------

## Canonical Data Model

All incoming events are transformed into:

``` json
{
  "user_identifier": "john@test.com",
  "consent_type": "EMAIL_MARKETING",
  "consent_status": "GRANTED",
  "event_timestamp": "2026-02-20T10:00:00",
  "source_system": "EVENT_PLATFORM",
  "external_event_id": "unique-event-id"
}
```

------------------------------------------------------------------------

## Database Schema

### Core Tables

-   users
-   consent_types
-   source_systems
-   consent_history (immutable ledger)
-   consent_current (materialized current state)
-   processed_events (idempotency tracking)

------------------------------------------------------------------------

## How to Run the Project

### Option 1: Run Locally

1.  Clone Repository

```{=html}
<!-- -->
```
    git clone https://github.com/your-username/UCMP.git
    cd UCMP

2.  Create Virtual Environment

```{=html}
<!-- -->
```
    python -m venv venv
    source venv/bin/activate

3.  Install Dependencies

```{=html}
<!-- -->
```
    pip install -r requirements.txt

4.  Create PostgreSQL Database

```{=html}
<!-- -->
```
    CREATE DATABASE ucmp;

5.  Run DDL Script

```{=html}
<!-- -->
```
    psql -d ucmp -f ddl.sql

6.  Start Application

```{=html}
<!-- -->
```
    uvicorn app.main:app --reload

Access API at: http://localhost:8000

Swagger Docs: http://localhost:8000/docs

------------------------------------------------------------------------

### Option 2: Run with Docker

    docker-compose build
    docker-compose up

------------------------------------------------------------------------

## API Endpoints

### POST /consents

Ingest consent event from any platform.

Example Request:

``` json
{
  "email": "john@test.com",
  "marketing_opt_in": true,
  "timestamp": "2026-02-20T10:00:00",
  "source": "event_platform"
}
```

Response:

``` json
{
  "message": "Consent processed successfully",
  "current_status": "GRANTED"
}
```

------------------------------------------------------------------------

### GET /users/{user_id}/consents

Fetch current consent state for a user.

------------------------------------------------------------------------

### GET /users/{user_id}/consents/history

Fetch full consent audit trail.

------------------------------------------------------------------------

### GET /consents/active?type=EMAIL_MARKETING

Fetch all users with active EMAIL_MARKETING consent.

------------------------------------------------------------------------

## Idempotency & Deduplication

-   Unique event_id tracking
-   processed_events table
-   Database-level primary key enforcement
-   UPSERT logic for current state

Duplicate events are ignored safely.

------------------------------------------------------------------------

## Late-Arriving Events

-   Older events are stored in consent_history
-   current_state updates only if event_timestamp is newer

------------------------------------------------------------------------

## Performance & Scalability

### Indexing Strategy

-   Composite index (user_id, consent_type_id)
-   Index (consent_type_id, current_status)

### Partitioning Strategy

-   consent_history partitioned by event_timestamp

### Scaling Strategy

-   RDS read replicas
-   SQS buffering (AWS deployment)
-   Lambda auto-scaling
-   S3 archival for cold data

------------------------------------------------------------------------

## Audit & Compliance

-   Immutable history ledger
-   Version tracking
-   Source tracking
-   Full historical retrieval
-   Supports GDPR / CCPA requirements

------------------------------------------------------------------------

## Future Improvements

-   Kafka streaming integration
-   DynamoDB high-scale variant
-   CDC to Redshift
-   Encryption & IAM-based access control
-   GDPR delete workflow

------------------------------------------------------------------------

## Author

Unified Consent Management Platform (UCMP) Scalable • Compliant •
Event-Driven Consent Architecture
