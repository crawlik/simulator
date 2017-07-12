import os
import logging
import atexit
import datetime
import random

from distutils.util import strtobool
import dateutil.parser

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from apscheduler.schedulers.background import BackgroundScheduler

from models import WeatherMetric
from database import db_session, init_db
from sqlalchemy.sql import func

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.INFO)

JOB_ID = 'generate data point job'
JOB_INTERVAL = 15  # seconds

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def generate_datapoint():
    wm = WeatherMetric(datetime.datetime.now(),
                       round(random.uniform(0, 50), 2),  # temperature
                       round(random.uniform(0, 100), 2),  # humidity
                       round(random.uniform(0, 100), 2),  # precipitation
                       round(random.uniform(0, 50), 2))  # wind
    db_session.add(wm)
    db_session.commit()


scheduler.add_job(
    generate_datapoint,
    'interval', seconds=JOB_INTERVAL,
    id=JOB_ID, max_instances=1,
    name='Simulate data',
    next_run_time=datetime.datetime.now(),
    replace_existing=True)

port = int(os.environ.get('PORT', 5000))


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


class Summary(Resource):
    def get(self):
        from_ts = dateutil.parser.parse(request.args.get('from_ts'))
        to_ts = dateutil.parser.parse(request.args.get('to_ts'))
        result = WeatherMetric.query \
            .with_entities(
            func.avg(WeatherMetric.temperature).label('avg-temperature'),
            func.min(WeatherMetric.temperature).label('min-temperature'),
            func.max(WeatherMetric.temperature).label('max-temperature'),
            func.avg(WeatherMetric.humidity).label('avg-humidity'),
            func.min(WeatherMetric.humidity).label('min-humidity'),
            func.max(WeatherMetric.humidity).label('max-humidity'),
            func.avg(WeatherMetric.precipitation).label('avg-precipitation'),
            func.min(WeatherMetric.precipitation).label('min-precipitation'),
            func.max(WeatherMetric.precipitation).label('max-precipitation'),
            func.avg(WeatherMetric.wind_speed).label('avg-wind-speed'),
            func.min(WeatherMetric.wind_speed).label('min-wind-speed'),
            func.max(WeatherMetric.wind_speed).label('max-wind-speed')) \
            .filter(WeatherMetric.collection_ts >= from_ts) \
            .filter(WeatherMetric.collection_ts <= to_ts) \
            .first()

        # quick and dirty
        # must be a better way to get dict from query
        summary = {'avg-temperature': float(result[0]),
                   'min-temperature': result[1],
                   'max-temperature': result[2],
                   'avg-humidity': float(result[3]),
                   'min-humidity': result[4],
                   'max-humidity': result[5],
                   'avg-precipitation': float(result[6]),
                   'min-precipitation': result[7],
                   'max-precipitation': result[8],
                   'avg-wind_speed': float(result[9]),
                   'min-wind_speed': result[10],
                   'max-wind_speed': result[11]}
        return jsonify(summary)


api.add_resource(Summary, '/summary')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
