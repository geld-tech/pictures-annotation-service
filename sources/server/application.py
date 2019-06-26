#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Service to annotate uploaded pictures using Keras and based on Python Flask and Vue.js.
"""
import ast
import base64
import ConfigParser
import logging
import logging.handlers
import os
import sys
from codecs import encode
from functools import wraps
from optparse import OptionParser

from celery import Celery
from flask import Flask, jsonify, render_template, request, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

from modules.Models import Base
from worker import identify

# Global config
local_path = os.path.dirname(os.path.abspath(__file__))
config_file = local_path+'/config/settings.cfg'
secret_file = local_path+'/config/secret.uti'
upload_dir = local_path+'/data/'
types_list = set(['bmp', 'ico', 'png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff'])
max_length = 8*1024*1024  # 8 MB
# broker_uri = 'amqp://%s:%s@%s/%s' % (os.environ['MQ_USER'], os.environ['MQ_PASS'], os.environ['MQ_HOST'], os.environ['MQ_VAPP'])
broker_uri = 'amqp://localhost//'

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')

# Shared secret for threads sessions
if os.path.isfile(secret_file):
    with open(secret_file, 'r') as file:
        secret_key = file.read()
else:
    generate_command = 'python -c  "import os; print os.urandom(24)" > %s' % secret_file
    logger.critical('Session secret does not exist! Generate it with: %s' % generate_command)
    sys.exit(-1)

# Flask Initialisation
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_dir
app.config['MAX_CONTENT_LENGTH'] = max_length
app.url_map.strict_slashes = False
app.secret_key = secret_key
app.debug = True

# Celery Initialisation
celery = Celery(app.name, broker=broker_uri)
celery.conf.update(app.config)
celery.conf.update(BROKER_POOL_LIMIT=None, CELERY_TASK_IGNORE_RESULT=True)
celery.conf.update(CELERY_BROKER_URL=broker_uri)
celery.task_default_queue = '__PACKAGE_NAME__'
logger.info("Celery application connected to: %s" % broker_uri)

# DB Session
db_path = local_path+'/data/metrics.sqlite3'
engine = create_engine('sqlite:///'+db_path)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


def authenticated(func):
    """Checks whether user is logged in or raises error 401."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('admin_user', False):
            return func(*args, **kwargs)
        else:
            return jsonify({"data": {}, "error": "Authentication required.", "authenticated": False}), 401
    return wrapper


@app.route("/")
def index():
    global config_file
    try:
        ganalytics_id = ''
        if os.path.isfile(config_file):
            settings = {'firstSetup': False}
            config = ConfigParser.ConfigParser()
            config.readfp(open(config_file))
            if 'ganalytics' in config.sections():
                ganalytics_id = config.get('ganalytics', 'ua_id')
        else:
            settings = {'firstSetup': True}
            # Bypass authentication during first setup
            session.clear()
            session['admin_user'] = True

        return render_template('index.html', settings=settings, ga_ua_id=ganalytics_id)
    except Exception, e:
        logger.error('Error serving web application: %s' % e)
        return jsonify({'data': {}, 'error': 'Could serve web application, check logs for more details..'}), 500


@app.route("/api/", strict_slashes=False)
def status():
    try:
        datasets = []
        time_labels = []
        xaxis_labels = []

        offset = 1  # GMT+1 as Default Timezone offset
        if request.headers.get('offset'):
            offset = int(request.headers.get('offset'))
        logger.debug("Timezone offeset: %s" % offset)

        return jsonify({'labels': xaxis_labels,
                        'datasets': datasets,
                        'time_labels': time_labels}), 200
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        del exc_type
        del exc_obj
        logger.error('Error retrieving status (line %d): %s' % (exc_tb.tb_lineno, e))
        return jsonify({'data': {}, 'error': 'Could not retrieve status, check logs for more details..'}), 500


@app.route("/setup/password/", methods=['POST'], strict_slashes=False)
@authenticated
def set_password():
    if request.method == 'POST':
        data = ast.literal_eval(request.data)
        if 'password' in data:
            password = sanitize_user_input(data['password'])
            if store_password(password):
                return jsonify({"data": {"response": "Success!"}}), 200
            else:
                return jsonify({"data": {}, "error": "Could not set password"}), 500
        else:
            return jsonify({"data": {}, "error": "Password needs to be specified"}), 500
    else:
        return jsonify({"data": {}, "error": "Incorrect request method"}), 500


def colors_generator():
    colors = ["#3E95BC", "#8E5EA2", "#3CBA9F", "#E8C3B9", "#C45850",
              "#FF6384", "#36A2EB", "#CC65FE", "#FFCE56", "#803690",
              "#00ADF9", "#DCDCDC", "#46BFBD", "#FDB45C", "#949FB1",
              "#4D5360", "#80B6F4", "#94D973", "#FAD874", "#F49080"]
    while True:
        for color in colors:
            yield color


@app.route("/auth/login/", methods=['POST'], strict_slashes=False)
def login():
    global config_file
    if request.method == 'POST':
        data = ast.literal_eval(request.data)
        if 'password' in data and os.path.isfile(config_file):
            config = ConfigParser.ConfigParser()
            config.readfp(open(config_file))
            if 'admin' in config.sections():
                current_password = config.get('admin', 'password')
                password = sanitize_user_input(data['password'])
                if obfuscate(password) == current_password:
                    session.clear()
                    session['admin_user'] = True
                    return jsonify({"data": {"response": "Login success!", "authenticated": True}}), 200
                else:
                    return jsonify({"data": {}, "error": "Unauthorised, authentication failure.."}), 401
            else:
                return jsonify({'data': {}, 'error': 'Could not retrieve current credentials..'}), 500
        else:
            return jsonify({"data": {}, "error": "Password needs to be specified"}), 500
    else:
        return jsonify({"data": {}, "error": "Incorrect request method"}), 500


@app.route("/auth/logout/", methods=['GET', 'POST'], strict_slashes=False)
@authenticated
def logout():
    try:
        session.clear()
        return jsonify({"data": {"response": "Logged out successfully!"}}), 200
    except Exception, e:
        logger.error('Error while logging out: %s' % e)
        return jsonify({'data': {}, 'error': 'Exception encountered while logging out..'}), 500


def store_password(password):
    global config_file
    try:
        config = ConfigParser.ConfigParser()
        if os.path.isfile(config_file):
            config.readfp(open(config_file))
            if 'admin' in config.sections():
                config.remove_section('admin')
        config.add_section('admin')
        config.set('admin', 'password', obfuscate(password))

        with open(config_file, 'w') as outfile:
            config.write(outfile)

        return True
    except Exception:
        return False


@app.route("/setup/ganalytics/", methods=['POST'], strict_slashes=False)
@authenticated
def set_ganalytics():
    if request.method == 'POST':
        data = ast.literal_eval(request.data)
        if 'uaid' in data:
            ua_id = sanitize_user_input(data['uaid'])
            if store_ua_id(ua_id):
                return jsonify({"data": {"response": "Success!"}}), 200
            else:
                return jsonify({"data": {}, "error": "Could not set UA ID"}), 500
        else:
            return jsonify({"data": {}, "error": "Google Analytics User Agent ID needs to be specified"}), 500
    else:
        return jsonify({"data": {}, "error": "Incorrect request method"}), 500


def get_ua_id():
    global config_file
    ua_id = ''
    try:
        if os.path.isfile(config_file):
            config = ConfigParser.ConfigParser()
            config.readfp(open(config_file))
            if 'ganalytics' in config.sections():
                ua_id = config.get('ganalytics', 'ua_id')
    except Exception, e:
        logger.error('Error while retrieving UA ID: %s' % e)
    finally:
        return ua_id


def store_ua_id(ua_id):
    global config_file
    try:
        config = ConfigParser.ConfigParser()
        if os.path.isfile(config_file):
            config.readfp(open(config_file))
            if 'ganalytics' in config.sections():
                config.remove_section('ganalytics')
        config.add_section('ganalytics')
        config.set('ganalytics', 'ua_id', ua_id)

        with open(config_file, 'w') as outfile:
            config.write(outfile)

        return True
    except Exception:
        return False


@app.route("/setup/config/", methods=['GET'], strict_slashes=False)
@authenticated
def get_config():
    if request.method == 'GET':
        ua_id = get_ua_id()
        return jsonify({"data": {"response": "Success!", "ua_id": ua_id}}), 200
    else:
        return jsonify({"data": {}, "error": "Incorrect request method"}), 500


def sanitize_user_input(word):
    black_list = ['__import__', '/', '\\', '&', ';']
    for char in black_list:
        word = word.replace(char, '')
    return word


def obfuscate(text, decode=False):
    try:
        if decode:
            return base64.b64decode(decode(text, 'rot13'))
        else:
            return base64.b64encode(encode(text, 'rot13'))
    except Exception, e:
        logger.error('Error while encoding or decoding text: %s' % e)
        return text


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        logger.info("Celery Status: %s" % is_celery_working())
        # Validations
        if 'files' not in request.files:
            return jsonify({"data": {}, "error": "No file part uploaded"}), 500
        files = request.files.getlist('files')
        for f in files:
            if f.filename == '':
                return jsonify({"data": {}, "error": "No selected files"}), 500
        for f in files:
            if not type_allowed(f.filename):
                return jsonify({"data": {}, "error": "Filetype not allowed"}), 500
        # Save file
        filenames = []
        for f in files:
            if f:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)
        # Sending task to MQ
        task = identify.apply_async(args=[filenames], queue="__PACKAGE_NAME__")
        logger.info("Celery Queued Task ID: %s" % task.task_id)
        return jsonify({"data": {"response": "Success!", "files": filenames}, "task_id": task.task_id}), 200
    else:
        return jsonify({"data": {}, "error": "Incorrect request method"}), 500


def type_allowed(filename):
    global types_list
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in types_list


def is_celery_working():
    result = celery.control.broadcast('ping', reply=True, limit=1)
    return bool(result)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404


if __name__ == "__main__":
    # Parse options
    opts_parser = OptionParser()
    opts_parser.add_option('--debug', action='store_true', dest='debug', help='Print verbose output.', default=False)
    options, args = opts_parser.parse_args()
    if options.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Enabled DEBUG logging level.')
    logger.info('Options parsed')
    app.run(host='0.0.0.0')
