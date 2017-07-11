import os
import logging
import atexit

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from apscheduler.schedulers.background import BackgroundScheduler

from distutils.util import strtobool

#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.INFO)

JOB_ID = 'generate data point job'
JOB_INTERVAL = 15

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


def generate_datapoint():
    print("generate_datapoint is called")

@app.before_first_request
def initialize():
    scheduler.add_job(
        generate_datapoint,
        'interval', seconds=JOB_INTERVAL,
        id=JOB_ID, max_instances=1,
        name='Simulate data',
        replace_existing=True)


port = int(os.environ.get('PORT', 5000))

#db = SQLAlchemy()


class Controller(Resource):
    def __status(self):
        job = scheduler.get_job(JOB_ID)
        return {'on': bool(job.next_run_time),
                'interval': job.trigger.interval.seconds}

    def get(self):
        return jsonify(self.__status())

    def put(self):
        on = bool(strtobool(request.args.get('on', 'True')))
        job = scheduler.get_job(JOB_ID)
        interval = int(request.args.get('interval',
                                        job.trigger.interval.seconds))
        if on:
            job.reschedule('interval', seconds=interval)
        else:
            job.pause()
        return jsonify(self.__status())


api.add_resource(Controller, '/controller')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
