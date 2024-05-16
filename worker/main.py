"""Module defining Celery tasks for fetching currencies."""

from worker import configure as worker_configure
from worker import tasks as worker_tasks


app = worker_configure.configure_app()


@app.task
def worker_get_currencies():
    """
    Celery task for fetching currencies using worker_tasks.get_currencies().

    This Celery task is responsible for fetching currencies using the
    worker_tasks.get_currencies() function.

    """
    worker_tasks.get_currencies()
