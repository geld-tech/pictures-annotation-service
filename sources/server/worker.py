#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Global variables
TMP_DIR = '/tmp'
broker_uri = 'amqp://%s:%s@%s/%s' % (os.environ['MQ_USER'], os.environ['MQ_PASS'], os.environ['MQ_HOST'], os.environ['MQ_VAPP'])

# Celery Initialisation
celery = Celery('__PACKAGE_NAME__', broker=broker_uri)
celery.conf.update(BROKER_POOL_LIMIT=None, CELERY_TASK_IGNORE_RESULT=True)


@celery.task
def identify(filename):
    ''' Identify picture provided '''
    try:
        print "Identifying file: %s" % filename
        return True
    except Exception:
        return False


@celery.task
def list():
    ''' List working directory contents '''
    return os.listdir(TMP_DIR)
