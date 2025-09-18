import smtplib
from email.message import EmailMessage
from typing import Optional
from .config import settings
from .templates_loader import render_template
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def build_message(to_email: str, subject: str, body_text: str, body_html: Optional[str], from_email: Optional[str]) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = from_email or settings.DEFAULT_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body_text)
    if body_html:
        msg.add_alternative(body_html, subtype = "html")
    return msg

def send_via_smtp(msg: EmailMessage):
    host = settings.MAIL_HOST
    port = settings.MAIL_PORT
    user = settings.MAIL_USER
    pwd = settings.MAIL_PASS

    logger.info("connecting to SMTP %s:%s", host, port)
    try:
        with smtplib.SMTP(host, port, timeout = 30) as smtp:
            if port == 587 or settings.MAIL_PROVIDER == "smtp":
                try:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                except Exception:
                    pass

            if user and pwd:
                smtp.login(user, pwd)
                            
            smtp.send_message(msg)
        logger.info("Email sent to %s", msg["to"])
    except Exception as e:
        logger.exception("SMTP send failed %s", e)
        raise

# SES via boto3
def send_ses_api(msg: EmailMessage):
    logger.info("SES API sending via region %s to %s", settings.AWS_REGION, msg["To"])
    ses = boto3.client(
        "ses",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    #create raw message bytes (for html alternative)
    raw = msg.as_bytes()
    try:
        resp = ses.send_raw_email(RawMessage={"Data": raw})
        logger.info("SES send_raw_email message id: %s", resp.get("MessageId"))
        return {"status": "sent", "message_id": resp.get("MessageId")}
    except ClientError as e:
        logger.exception("SES send failed: %s", e)
        raise

# Used by tasks
def send_via_selected_provider(msg: EmailMessage):
    if settings.MAIL_PROVIDER == "ses-api":
        return send_ses_api(msg)
    else:
        return send_via_smtp(msg)

def send_email_raw(to: str, subject: str, body_text: str, body_html: Optional[str] = None, from_email: Optional[str] = None):
    msg = build_message(to, subject, body_text, body_html, from_email)
    send_via_smtp(msg)

def send_using_template(template_name: str, to: str, subject: str, context: dict, from_email: Optional[str]=None):
    body_text = ""
    body_html = None
    try:
        # try .txt
        body_text = render_template(template_name + ".txt", context)
    except Exception:
        # if not found, fallback to rendering html as text
        try:
            body_text = render_template(template_name + ".html", context)
        except Exception:
            body_text = ""

    try:
        body_html = render_template(template_name + ".html", context)
    except Exception:
        body_html = None

    if not body_text and not body_html:
        raise ValueError("No templates found for %s" % template_name)

    return send_email_raw(to, subject, body_text, body_html, from_email)