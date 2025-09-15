from pydantic import BaseModel, EmailStr
from typing import Dict, Optional

class SendEmailRequest(BaseModel):
    to: EmailStr
    subject: str
    template: Optional[str] = None  # e.g., "otp" or "welcome"
    context: Dict[str, str] = {}
    from_email: Optional[EmailStr] = None
    request_id: Optional[str] = None  # optional idempotency token