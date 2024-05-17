"""Module for configuring Celery application."""

import celery
from components.core import config
from celery.schedules import crontab

WORKER_TASK_QUEUE = "worker-queue"
WORKER_ROUTING_KEY = "worker"
WORKER_TIMEZONE = "UTC"

cnfg = config.config


def configure_app() -> celery.Celery:
    """
    Configure and initialize the Celery application.

    Returns:
        celery.Celery: The configured Celery application instance.

    """
    app = celery.Celery(
        "worker",
        broker=cnfg.REDIS_URL,
        backend=cnfg.REDIS_URL,
    )
    app.conf.task_default_queue = WORKER_TASK_QUEUE
    app.conf.task_default_routing_key = WORKER_ROUTING_KEY  # type: ignore
    app.conf.timezone = WORKER_TIMEZONE  # type: ignore

    app.conf.broker_transport_options = {
        "visibility_timeout": 1800,
        "health_check_interval": 30,
    }

    app.conf.beat_schedule = {
        "worker.": {
            "task": "main.worker_get_currencies",
            "schedule": crontab(minute="*/15"),
        }
    }

    return app
