import asyncio
import requests
from models import JobResponse, Status, TranslationRequest
from services.webhook_service import WebhookService


class TranslationService:
    BASE_URL = "http://localhost:5000/translations/status"
    
    @staticmethod
    async def create_translation(request: TranslationRequest) -> JobResponse:
        response = requests.post(
            f"{TranslationService.BASE_URL}/",
            json=request.dict(),
            timeout=2,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return JobResponse(**response.json())

    @staticmethod
    async def get_job(job_id: str) -> JobResponse:
        response = requests.get(
            f"{TranslationService.BASE_URL}/{job_id}",
            timeout=2,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return JobResponse(**response.json())

    @staticmethod
    async def monitor_job_status(job: JobResponse):
        while True:
            job = await TranslationService.get_job(job.id)
            current_status = job.status

            if current_status in [Status.COMPLETED, Status.ERROR]:
                await WebhookService.send_webhook(job)
                return
            await asyncio.sleep(1)