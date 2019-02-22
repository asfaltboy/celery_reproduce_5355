from celery import Celery
from celery.signals import task_prerun

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task()
def add(x, y):
    print(x + y)
    return x + y


@app.task(queue='custom')
def multiply(x, y):
    print(x * y)
    return x * y


@task_prerun.connect()
def task_prerun(sender=None, task_id=None, task=None, **kwargs):
    """ Log out some meta-info on the task being handled by worker """
    print(
        f"Handling {task.name} - {task_id} on queue: "
        f"{sender.request.delivery_info['routing_key']}"
    )


app.conf.beat_schedule = {
    'add-every-2-seconds': {
        'task': 'tasks.add',
        'schedule': 2.0,
        'args': (16, 16)
    },
    'multiple-every-2-seconds': {
        'task': 'tasks.multiply',
        'schedule': 2.0,
        'args': (5, 5)
    },
}
app.conf.timezone = 'UTC'
