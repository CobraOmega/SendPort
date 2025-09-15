from fastapi import APIRouter, HTTPException, BackgroundTasks, Header
from .schemas import SendEmailRequest
from .utils import send_using_template, send_email_raw
from .config import settings
from typing import Optional
import uuid

router = APIRouter()

def check_api_key(x_api_key: Optional[str]):
    if not x_api_key or x_api_key != settings.SERVICE_API_KEY:
        return False
    return True

@router.post("/v1/send-email")
async def send_email_endpoint(payload: SendEmailRequest, background_tasks: BackgroundTasks, x_api_key: Optional[str] = Header(None)):
    if not check_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Generate job ID or reuse request_id
    job_id = str(payload.request_id or uuid.uuid4())

    # Choose template or raw body
    if payload.template:
        # background send using template
        background_tasks.add_task(send_using_template, payload.template, payload.to, payload.subject, payload.context, payload.from_email)
    else:
        # raw body: use context['body'] as plaintext
        body = payload.context.get("body") if payload.context else " "
        background_tasks.add_task(send_email_raw, payload.to, payload.subject, body, None, payload.from_email)

    return {"job_id": job_id, "status": "queued"}