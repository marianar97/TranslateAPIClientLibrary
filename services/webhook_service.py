import asyncio
import requests
from models import JobResponse


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
                print(f"Webhook attempt {attempt + 1} failed with error: {e}")
            
            await asyncio.sleep(WebhookService.RETRY_DELAY * (2**attempt))

        return False