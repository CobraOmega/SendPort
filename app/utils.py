# helper functions

import smtplib
from email.message import EmailMessage
from typing import Optional
from .config import settings
from .templates_loader import render_template
import logging

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
    host = settings.SMTP_HOST
    port = settings.SMTP_PORT
    user = settings.SMTP_USER
    pwd = settings.SMTP_PASS

    logger.info("connecting to SMTP %s:%s", host, port)
    try:
        with smtplib.SMTP(host, port, timeout = 30) as smtp:
            #Use TLS for port
            if port == 587:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
            if user and pwd:
                smtp.login(user, pwd)
            smtp.send_message(msg)
        logger.info("Email sent to %s", msg["to"])
    except Exception as e:
        logger.exception("SMTP send failed %s", e)
        raise

def send_email_raw(to: str, subject: str, body_text: str, body_html: Optional[str] = None, from_email: Optional[str] = None):
    msg = Build_Message(to, subject, body_text, body_html, from_email)
    send_via_smtp(msg)

def send_using_template(template_name: str, to: str, subject: str, context: dict, from_email: Optional[str]=None):
    body_text = ""
    body_html = None
    try:
        # Try .txt
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

    send_email_raw(to, subject, body_text, body_html, from_email)