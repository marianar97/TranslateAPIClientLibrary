import asyncio
import datetime
from enum import Enum
import json
import time
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import UUID4, BaseModel, Field
import requests


class JobResponse(BaseModel):
    id: str
    webhook_url: str
    created_at: datetime.datetime
    duration: float
    status: str


class Status(str, Enum):
    PENDING = "pending"
    ERROR = "error"
    COMPLETED = "completed"


class TranslationRequest(BaseModel):
    duration: float = Field(description="configurable delay in seconds")
    webhook_url: str = Field(
        description="url endpoint to notify once the translation is completed"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"duration": 30.5, "webhook_url": "https://webhook.site/94070b61-3ca5-4a17-8fc0-db7b8a8c1c8c"}
            ]
        }
    }


class WebhookService:
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds

    @staticmethod
    async def send_webhook(job: JobResponse) -> bool:
        if not job.webhook_url:
            return True

        payload = {
            "job_id": job.id,
            "status": job.status,
            "created_at": str(job.created_at),
            "event_type": "translation.status_update",
        }

        for attempt in range(WebhookService.MAX_RETRIES):
            try:
                response = requests.post(
                    job.webhook_url,
                    json=payload,
                    timeout=5,
                    headers={"Content-Type": "application/json"},
                )
                if response.ok:
                    print("sent webhook")
                    return True

            except requests.RequestException as e:
                print("ERROR")
            job.webhook_attempts += 1
            await asyncio.sleep(WebhookService.RETRY_DELAY * (2**attempt))

        return False


async def _monitor_job_status(job: JobResponse):
    while True:
        job = await get_status(job.id)
        current_status = job.status

        if current_status in [Status.COMPLETED, Status.ERROR]:
            await WebhookService.send_webhook(job)
            return
        await asyncio.sleep(1)

app = FastAPI()

    
async def get_status(job_id: str) -> JobResponse:
    response = requests.get(
        f"http://localhost:5000/translations/status/{job_id}",
        timeout=5,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return JobResponse(**response.json())

    MAX_ATTEMPTS = 3
    RETRY_DELAY = 1  # seconds

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = requests.get(
                f"http://localhost:5000/translations/status/{id}",
                timeout=5,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()  # Raises an exception for 4XX/5XX status codes

            job = JobResponse(**response.json())
            return job
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < MAX_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY * (2**attempt))  # Exponential backoff

    return None


async def _create_translation(request: TranslationRequest) -> JobResponse:
    response = requests.post(
        "http://127.0.0.1:5000/translations/status/",
        json=request.dict(),
        timeout=2,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    print("returning")
    return JobResponse(**response.json())


@app.post("/translations/job/", status_code=201)
async def create_translation_job(
    request: TranslationRequest, background_tasks: BackgroundTasks
) -> JobResponse:
    job = await _create_translation(request)
    background_tasks.add_task(_monitor_job_status, job)
    return job
