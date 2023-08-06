import logging.config
import os
import time
from importlib import import_module

from flask import Flask
from flask.logging import default_handler
from flask_coralillo import Coralillo
from flask_cors import CORS

from cacahuate.indexes import create_indexes
from cacahuate.models import bind_models
from cacahuate.http.mongo import mongo
from cacahuate.tasks import app as celery

# The flask application
app = Flask(__name__)
app.config.from_object('cacahuate.settings')
app.config.from_envvar('CACAHUATE_SETTINGS', silent=True)

# Setup logging
app.logger.removeHandler(default_handler)
logging.config.dictConfig(app.config['LOGGING'])

# Enalble cross origin
CORS(app)

# Timezone
os.environ['TZ'] = app.config.get('TIMEZONE', 'UTC')
time.tzset()

# Bind the redis database
cora = Coralillo(
    app,
    id_function=getattr(
        import_module(app.config['DB_ID_FUNCTION'].rsplit('.', 1)[0]),
        app.config['DB_ID_FUNCTION'].rsplit('.', 1)[1],
    ),
)
bind_models(cora._engine)

# The mongo database
mongo.init_app(app)
create_indexes(app.config)

celery.conf.update(
    broker='amqp://{user}@{host}//'.format(
        user=app.config['RABBIT_USER'],
        host=app.config['RABBIT_HOST'],
    ),
    task_default_queue=app.config['RABBIT_QUEUE'],
)

# Url converters
import cacahuate.http.converters  # noqa

# Views
import cacahuate.http.views.api  # noqa
app.register_blueprint(cacahuate.http.views.api.bp, url_prefix=app.config['URL_PREFIX'])
import cacahuate.http.views.auth  # noqa
app.register_blueprint(cacahuate.http.views.auth.bp, url_prefix=app.config['URL_PREFIX'])
import cacahuate.http.views.templates  # noqa
app.register_blueprint(cacahuate.http.views.templates.bp, url_prefix=app.config['URL_PREFIX'])
if app.config['SSE_ENABLED']:
    import flask_sse
    app.register_blueprint(flask_sse.sse, url_prefix='/stream')

# Error handlers
import cacahuate.http.error_handlers  # noqa
