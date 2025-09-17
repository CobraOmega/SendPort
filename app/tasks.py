from app.celery_app import celery_app
from app.utils import send_email_raw, send_using_template


@celery_app.task(name="app.tasks.send_email_raw_task")
def send_email_raw_task(to, subject, body_text, body_html=None, from_email=None):
    try:
        return send_email_raw(to, subject, body_text, body_html, from_email)
    except Exception as e:
        raise send_email_raw_task.retry(exc=e)


@celery_app.task(name="app.tasks.send_using_template_task")
def send_template_task(template_name, to, subject, context, from_email=None):
    return send_using_template(template_name, to, subject, context, from_email)