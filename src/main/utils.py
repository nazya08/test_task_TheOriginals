import logging

from pathlib import Path
from typing import Any, Dict
from src.main.celery import celery_app

import emails
from emails.template import JinjaTemplate

from src.main.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert (
        settings.EMAILS_ENABLED
    ), "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    try:
        response = message.send(
            to=email_to, render=environment, smtp=smtp_options
        )
    except Exception as e:
        logging.info(f"ERROR: {e}")
    logging.info(f"send email result: {response}")


@celery_app.task
def send_status_change_email(email_to, task_title, old_status, new_status, due_date):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Task Status Update: {task_title}"

    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "task_status_change_email.html") as f:
        template_str = f.read()

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": project_name,
            "email": email_to,
            "task_title": task_title,
            "old_status": old_status,
            "new_status": new_status,
            "due_date": due_date.strftime('%Y-%m-%d') if due_date else 'No due date'
        },
    )


def mock_send_status_change_email(
        email_to: str,
        task_title: str,
        old_status: int,
        new_status: int,
        due_date: str
):
    print(f"Mock email sent to {email_to}")
    print(f"Subject: Status Change Notification for '{task_title}'")
    print(f"Body: The status has changed from {old_status} to {new_status}. Due date: {due_date}.")

