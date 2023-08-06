from os import path

from coralillo.errors import ModelNotFoundError

import flask

from jinja2 import Environment, FileSystemLoader, select_autoescape

from cacahuate.http.mongo import mongo
from cacahuate.mongo import make_context


bp = flask.Blueprint('template', __name__)


def datetimeformat(value, format='%Y-%m-%d %H:%M:%S%z'):
    return value.strftime(format)


@bp.route('/execution/<id>/summary', methods=['GET'])
def execution_template(id):
    # load values
    collection = mongo.db[flask.current_app.config['EXECUTION_COLLECTION']]

    try:
        execution = next(collection.find({'id': id}))
    except StopIteration:
        raise ModelNotFoundError(
            'Specified execution never existed, and never will'
        )

    if 'process_name' not in execution:
        return 'Not supported for old processes', 409

    context = make_context(execution, flask.current_app.config)

    # load template
    process_name = execution['process_name']
    name, version, _ = process_name.split('.')

    # Loaders will be inserted in inverse order and then reversed. The fallback
    # is the default template at ``templates/summary.html``
    paths = [
        path.join(path.dirname(path.realpath(__file__)), '../../templates'),
    ]

    app_template_path = flask.current_app.config['TEMPLATE_PATH']
    if app_template_path is not None and path.isdir(app_template_path):
        paths.append(app_template_path)

        process_dir = path.join(app_template_path, name)
        if path.isdir(process_dir):
            paths.append(process_dir)

        process_version_dir = path.join(
            process_dir, version
        )
        if path.isdir(process_version_dir):
            paths.append(process_version_dir)

    env = Environment(
        loader=FileSystemLoader(reversed(paths)),
        autoescape=select_autoescape(['html', 'xml'])
    )

    env.filters['datetimeformat'] = datetimeformat

    for name, function in flask.current_app.config['JINJA_FILTERS'].items():
        env.filters[name] = function

    return flask.make_response(
        env.get_template('summary.html').render(**context),
        200,
    )
