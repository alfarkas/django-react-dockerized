from __future__ import absolute_import, unicode_literals
from celery import shared_task

#import sentry_sdk
#from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk import capture_message
#from celery.utils.log import get_task_logger
#logger = get_task_logger(__name__)

#sentry_sdk.init("https://e2775ea58ea34b90843daa496c22b068@sentry.io/1860009", integrations=[CeleryIntegration()])

@shared_task
def hello():
    #logger = get_task_logger(__name__)
    #print(logger)
    #capture_message("Error example!", level="error")
    print("Hello there!")