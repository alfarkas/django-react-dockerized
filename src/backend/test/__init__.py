import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init("https://e2775ea58ea34b90843daa496c22b068@sentry.io/1860009", integrations=[CeleryIntegration()])