from fastapi import APIRouter, HTTPException, BackgroundTasks, Header

from app import celery_app
from .schemas import SendEmailRequest
from .utils import send_using_template, send_email_raw
from .config import settings
from typing import Optional
import uuid
from .tasks import send_email_raw_task, send_template_task
from celery.result import AsyncResult

router = APIRouter()

def check_api_key(x_api_key: Optional[str]):
    if not x_api_key or x_api_key != settings.SERVICE_API_KEY:
        return False
    return True

@router.post("/send-email")
async def send_email_endpoint(payload: SendEmailRequest, x_api_key: Optional[str] = Header(None)):
    if not check_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    job_id = str(payload.request_id or uuid.uuid4())

    if payload.template:
        send_template_task.delay(payload.template, payload.to, payload.subject, payload.context, payload.from_email)
    else:
        body = payload.context.get("body") if payload.context else " "
        send_email_raw_task.delay(payload.to, payload.subject, body, None, payload.from_email)

    return {"job_id": job_id, "status": "queued"}

@router.get("/task-status/{job_id}")
async def get_task_status(job_id: str):
    res = AsyncResult(job_id, app=celery_app)
    return {"job_id": job_id, "status": res.status, "result": res.result}