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

import platform
import sys
import cv2


# Debug Environment
print("System", platform.system(), "-", platform.release())
print("Executable", sys.executable)
print("Python", platform.python_version())
print("OpenCV", cv2.__version__)

# Global variables
local_path = os.path.dirname(os.path.abspath(__file__))
config_file = local_path+'/config/settings.cfg'
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
    records = {}
    logger.info("Received Request: ID=%s - Parameters=%s" % (self.request.id, filenames))
    self.update_state(state=states.PENDING)
    try:
        # Stores all requested files in pending state
        for filename in filenames:
            records[filename] = Picture(task_id=self.request.id, filename=filename, status="PENDING")
            db_session.add(records[filename])
            db_session.commit()
        # Process requested files then update status
        for filename in filenames:
            logger.info("Identifying: %s" % filename)
            records[filename].identification = identify_picture(filename)
            records[filename].status = "SUCCESS"
            db_session.commit()
        self.update_state(state=states.SUCCESS)
        return True
    except Exception, e:
        self.update_state(state=states.FAILURE)
        logger.error("Failed!")
        logger.warning("Exception: %s" % e)
        for filename in filenames:
            if records[filename].status != "SUCCESS":
                records[filename].status = "FAILED"
                db_session.commit()
        return False


@celery.task
def list():
    ''' List working directory contents '''
    return os.listdir(TMP_DIR)


def identify_picture(filename):
    ''' Identify picture provided '''
    global config_file
    settings = {'model': 'model.h5'}
    if os.path.isfile(config_file):
        config = ConfigParser.ConfigParser()
        config.readfp(open(config_file))
        if 'model' in config.sections():
            settings['model'] = config.get('model', 'file')
    logger.info("Loading Model %s" % settings['model'])
    return "cat"
