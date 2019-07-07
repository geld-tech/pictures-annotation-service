#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import logging
import logging.handlers
import os
import socket

from celery import Celery, states
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.Models import Base, Picture, Server

# Global variables
local_path = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = '/tmp'

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')
hostname = socket.gethostname()

# DB Session
db_path = local_path+'/data/metrics.sqlite3'
engine = create_engine('sqlite:///'+db_path)
Base.metadata.bind = engine
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
db_session = DBSession()
server = Server(hostname=hostname)
db_session.add(server)
db_session.commit()

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
    for filename in filenames:
        record = Picture(task_id=self.request.id, filename=filename, status="PENDING")
        db_session.add(record)
        db_session.commit()
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
