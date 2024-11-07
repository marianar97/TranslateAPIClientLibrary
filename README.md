# FastAPI Translation Service

A robust FastAPI application that manages translation jobs with webhook notifications. This service provides an asynchronous API for submitting translation jobs, monitoring their status, and receiving webhook notifications upon completion.

## Features

- 🚀 Asynchronous job processing
- 📊 Job status monitoring
- 🔔 Webhook notifications with retry mechanism
- ⚡ FastAPI-powered REST API
- 🏗️ Modular and maintainable architecture

## Project Structure

```
app/
├── __init__.py
├── main.py          # FastAPI application and routes
├── models.py        # Pydantic models and enums
└── services/
    ├── translation_service.py  # Translation-related operations
    └── webhook_service.py      # Webhook handling and retries
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Requests
- Pydantic

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-translation-service.git
cd fastapi-translation-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. The API will be available at `http://localhost:8000`

3. Access the interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### Create Translation Job

```http
POST /translations/job/
```

Request body:
```json
{
    "duration": 30.5,
    "webhook_url": "https://your-webhook-endpoint.com/callback"
}
```

Response:
```json
{
  "id": "97fabbb7-6f5c-49f0-964d-cf7feca5642c",
  "webhook_url": "https://your-webhook-endpoint.com/callback",
  "created_at": "2024-11-07T00:53:39.054062Z",
  "duration": 30.5,
  "status": "pending"
}
```

## Webhook Notifications

Upon job completion or error, the service will send a webhook notification to the specified URL with the following payload:

```json
{
  "job_id": "e39e4668-ea7a-4fea-af92-efd65200a256",
  "status": "completed",
  "created_at": "2024-11-07 00:39:06.562608+00:00",
  "event_type": "translation.status_update"
}
```

The webhook service includes:
- Maximum of 3 retry attempts
- Exponential backoff between retries
- 5-second timeout for each attempt

## Configuration

Key configuration values can be found in their respective service files:

- `WebhookService`:
  - `MAX_RETRIES = 3`
  - `RETRY_DELAY = 5` (seconds)

- `TranslationService`:
  - `BASE_URL = "https://translationapibackend.onrender.com/translations/status"`


## Error Handling

The service includes robust error handling for:
- Failed webhook deliveries
- Translation API communication issues
- Invalid requests
- Timeouts
