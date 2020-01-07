from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery import bootsteps
from celery.bin import Option
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

#def add_worker_arguments(parser):
#    parser.add_argument(
#        '--enable-my-option', action='store_true', default=False,
#        help='Enable custom option.',
#    ),
#app.user_options['worker'].add(add_worker_arguments)
#app.user_options['beat'].add(add_worker_arguments)
app.user_options['worker'].add(
    Option('--sentry', dest='dsn', default=None, help='Sentry DSN.')
)
app.user_options['beat'].add(
    Option('--sentry', dest='dsn', default=None, help='Sentry DSN.')
)

class CustomArgs(bootsteps.Step):

    def __init__(self, worker_beat, dsn, **options):
        # initialize sentry for celery
        if dsn:
            sentry_sdk.init(dsn[0], integrations=[CeleryIntegration()])


app.steps['worker'].add(CustomArgs)
app.steps['beat'].add(CustomArgs)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))