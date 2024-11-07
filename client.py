from fastapi import FastAPI, BackgroundTasks
from models import TranslationRequest, JobResponse
from services.translation_service import TranslationService

app = FastAPI()


@app.post("/translations/job/", status_code=201)
async def create_translation_job(
    request: TranslationRequest, background_tasks: BackgroundTasks
) -> JobResponse:
    job = await TranslationService.create_translation(request)
    background_tasks.add_task(TranslationService.monitor_job_status, job)
    return job

@app.get("/translation/job/{id}", status_code=200)
async def get_job(id: str):
    return await TranslationService.get_job(id)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)