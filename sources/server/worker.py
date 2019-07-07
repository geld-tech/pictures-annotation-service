#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import logging
import logging.handlers
import os

from celery import Celery, states

from modules.Models import Base

# Global variables
local_path = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = '/tmp'

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')


# DB Session
db_path = local_path+'/data/metrics.sqlite3'
engine = create_engine('sqlite:///'+db_path)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Celery Initialisation
# broker_uri = 'amqp://%s:%s@%s/%s' % (os.environ['MQ_USER'], os.environ['MQ_PASS'], os.environ['MQ_HOST'], os.environ['MQ_VAPP'])
broker_uri = 'amqp://localhost//'
celery = Celery('__PACKAGE_NAME__', broker=broker_uri)
celery.conf.update(BROKER_POOL_LIMIT=None, CELERY_TASK_IGNORE_RESULT=True)
celery.conf.update(CELERY_BROKER_URL=broker_uri)
celery.task_default_queue = '__PACKAGE_NAME__'
logger.info("Celery worker connected to: %s" % broker_uri)


@celery.task(bind=True)
def identify(self, filenames):
    ''' Identify provided pictures '''
    logger.info("Received Request: ID=%s - Parameters=%s" % (self.request.id, filenames))
    self.update_state(state=states.PENDING)
    try:
        logger.info("Identifying files: %s" % filenames)
        self.update_state(state=states.SUCCESS)
        return True
    except Exception:
        logger.error("Failed!")
        self.update_state(state=states.FAILURE)
        return False


@celery.task
def list():
    ''' List working directory contents '''
    return os.listdir(TMP_DIR)
