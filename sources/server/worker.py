#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import logging
import logging.handlers
import os

from celery import Celery, states

# Global variables
TMP_DIR = '/tmp'

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')

# Celery Initialisation
# broker_uri = 'amqp://%s:%s@%s/%s' % (os.environ['MQ_USER'], os.environ['MQ_PASS'], os.environ['MQ_HOST'], os.environ['MQ_VAPP'])
broker_uri = 'amqp://localhost/'
celery = Celery('__PACKAGE_NAME__', broker=broker_uri)
celery.conf.update(BROKER_POOL_LIMIT=None, CELERY_TASK_IGNORE_RESULT=True)
celery.task_default_queue = '__PACKAGE_NAME__'
logger.info("Celery worker connected to: %s" % broker_uri)


@celery.task(bind=True)
def identify(self, filenames):
    ''' Identify provided pictures '''
    self.update_state(state=states.PENDING)
    try:
        logger.info("Identifying files: %s" % filenames)
        return True
    except Exception:
        logger.error("Failed!")
        return False


@celery.task
def list():
    ''' List working directory contents '''
    return os.listdir(TMP_DIR)
