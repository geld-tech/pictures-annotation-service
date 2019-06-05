#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Global variables
TMP_DIR = '/tmp'

# Celery Initialisation
broker_uri = 'amqp://%s:%s@%s/%s' % (os.environ['MQ_USER'], os.environ['MQ_PASS'], os.environ['MQ_HOST'], os.environ['MQ_VAPP'])
celery = Celery('__PACKAGE_NAME__', broker=broker_uri)
celery.conf.update(BROKER_POOL_LIMIT=None, CELERY_TASK_IGNORE_RESULT=True)
print "Celery connected to: %s" % broker_uri


@celery.task
def identify(filenames):
    ''' Identify provided pictures '''
    try:
        print "Identifying files: %s" % filenames
        return True
    except Exception:
        return False


@celery.task
def list():
    ''' List working directory contents '''
    return os.listdir(TMP_DIR)
