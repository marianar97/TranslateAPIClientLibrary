from enum import Enum
import datetime
from pydantic import BaseModel, Field


class Status(str, Enum):
    PENDING = "pending"
    ERROR = "error"
    COMPLETED = "completed"


class JobResponse(BaseModel):
    id: str
    webhook_url: str
    created_at: datetime.datetime
    duration: float
    status: str


class TranslationRequest(BaseModel):
    duration: float = Field(description="configurable delay in seconds")
    webhook_url: str = Field(
        description="url endpoint to notify once the translation is completed"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "duration": 30.5,
                    "webhook_url": "https://webhook.site/94070b61-3ca5-4a17-8fc0-db7b8a8c1c8c"
                }
            ]
        }
    }
