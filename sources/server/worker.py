#!/usr/bin/env python
import atexit
import ConfigParser
import datetime
import os
import sys
import time

from daemon import runner
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.Models import Base, Metrics, Server, Service
from modules.ServiceStatus import ServiceStatus


class Worker():
    def __init__(self, pid_file, db_path, config_file, poll_interval=60, debug=True):
        self.stdin_path = '/dev/null'
        if debug:
            self.stdout_path = '/dev/tty'
            self.stderr_path = '/dev/tty'
            self.poll_interval = int(poll_interval/3)
        else:
            self.stdout_path = '/dev/null'
            self.stderr_path = '/dev/null'
            self.poll_interval = poll_interval
        self.pidfile_timeout = 5
        self.pidfile_path = pid_file
        self.db_path = db_path
        self.config_file = config_file
        self.db_session = None
        self.server = None
        self.services = []
        atexit.register(self.db_close)

    def run(self):
        try:
            print "creating DB..."
            # Initialise object to collect metrics
            services_status = ServiceStatus()
            # Connect to database
            self.db_open(services_status.get_server_hostname())

            # Hold off until configuration file created
            print "Sleeping until configuration file found (%s)" % self.config_file
            while True:
                if os.path.isfile(self.config_file):
                    break
                else:
                    time.sleep(self.poll_interval)

            print "Configuration file found, polling.."
            # First metrics poll to instantiate system information
            while True:
                # Poll and store
                dt = datetime.datetime.utcnow()
                services = self.get_services(self.config_file)
                data = services_status.poll_metrics(services)
                self.store_status(dt, data)
                time.sleep(self.poll_interval)
        except Exception, e:
            print "Collector error: %s" % e

    def db_open(self, hostname='localhost'):
        engine = create_engine('sqlite:///'+self.db_path)
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        self.db_session = DBSession()

        self.server = Server(hostname=hostname)
        self.db_session.add(self.server)
        self.db_session.commit()

    def db_close(self):
        if self.db_session:
            self.db_session.close()

    def db_rollback(self):
        self.db_session.rollback()

    def get_services(self, config_file):
        services = list()
        try:
            config = ConfigParser.ConfigParser()
            config.read(config_file)
            if 'services' in config.sections():
                for service in config.items('services'):
                    name = service[0]
                    url = service[1]
                    services.append({'name': name, 'url': url})
            return services
        except Exception, e:
            print "Exception while reading services from configuration: %s" % e
            return False

    def get_services_last2hours(self):
        try:
            now = datetime.datetime.utcnow()
            last_2_hours = now - datetime.timedelta(hours=2)
            self.services = self.db_session.query(Service).filter_by(server=self.server).filter(Service.timestamp >= last_2_hours.strftime('%s')).order_by(Service.id)
        except Exception:
            print "Error accessing services status"

    def store_status(self, date_time, data):
        try:
            for service in data:
                service_status = Metrics(timestamp=date_time.strftime('%s'),
                                         latency=data[service].get('latency', -1),
                                         available=data[service].get('reachable'),
                                         service_name=service)
                self.db_session.add(service_status)
                self.db_session.commit()
        except Exception, e:
            print "Error storing services status: %s" % e
        finally:
            self.db_close()


def is_running(pid_file):
    try:
        with file(pid_file, 'r') as pf:
            pid = int(pf.read().strip())
    except IOError:
        pid = None
    except SystemExit:
        pid = None

    if pid:
        return True, pid
    else:
        return False, -1


# Main
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
DB_FILE = SCRIPT_PATH + '/data/metrics.sqlite3'
CFG_FILE = SCRIPT_PATH + '/config/settings.cfg'
PID_FILE = SCRIPT_PATH + '/.__PACKAGE_NAME__-collector.pid'
POLL_INTERVAL = 30
DEBUG = False

if __name__ == "__main__":
    if len(sys.argv) == 3:
        DEBUG = True
    if len(sys.argv) >= 2:
        if 'status' == sys.argv[1]:
            running, pid = is_running(PID_FILE)
            if running:
                print '%s is running as pid %s' % (sys.argv[0], pid)
            else:
                print '%s is not running.' % sys.argv[0]
        elif 'stop' == sys.argv[1] and not is_running(PID_FILE)[0]:
            print '%s is not running.' % sys.argv[0]
        else:
            worker = Worker(PID_FILE, DB_FILE, CFG_FILE, poll_interval=POLL_INTERVAL, debug=DEBUG)
            daemon = runner.DaemonRunner(worker)
            daemon.do_action()  # start|stop|restart as sys.argv[1]
            running, pid = is_running(PID_FILE)
            sys.exit(0)
    else:
        print "Usage: %s start|stop|restart|status" % sys.argv[0]
        sys.exit(2)
else:
    print "%s can't be included in another program." % sys.argv[0]
    sys.exit(1)
