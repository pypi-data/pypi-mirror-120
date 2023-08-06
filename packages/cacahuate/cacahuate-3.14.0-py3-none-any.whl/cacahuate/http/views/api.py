import http
import re
import os

from cacahuate.mongo import make_context

import flask
from flask import g
from flask import request, jsonify, json
from flask_sse import sse

import pymongo
from simplejson.errors import JSONDecodeError

from coralillo.errors import ModelNotFoundError

from cacahuate.errors import InputError, RequiredListError, RequiredDictError
from cacahuate.errors import RequiredInputError, RequiredStrError
from cacahuate.errors import InvalidInputError
from cacahuate.errors import ProcessNotFound, ElementNotFound, MalformedProcess
from cacahuate.http.errors import BadRequest, NotFound, UnprocessableEntity
from cacahuate.http.errors import Forbidden
from cacahuate.http.middleware import requires_json, requires_auth, pagination
from cacahuate.http.validation import validate_json, validate_auth
from cacahuate.http.wsgi import mongo
from cacahuate.models import Execution, Pointer, User
from cacahuate.node import make_node
from cacahuate.xml import Xml, form_to_dict, get_text, get_element_by
from cacahuate.node import make_input
from cacahuate.mongo import json_prepare
from cacahuate.tasks import handle


# TODO: is this really required? maybe get doesn't need to support search
def format_query(q):
    try:
        formated_q = json.loads(q)
    except JSONDecodeError:
        formated_q = q
    return formated_q


bp = flask.Blueprint('cacahuate', __name__)


@bp.route('/', methods=['GET', 'POST'])
@requires_json
def index():
    ''' This is here to provide a successful response for the / url and also to
    provide a test for the json middleware '''
    if request.method == 'GET':
        return {
            'hello': 'world',
        }
    elif request.method == 'POST':
        return request.json


@bp.route('/user/<user_identifier>', methods=['GET'])
def fetch_user_info(user_identifier):
    user = User.get_by('identifier', user_identifier)

    if user is None:
        flask.abort(404)

    return flask.make_response(
        flask.jsonify({
            'identifier': user.get_contact_info('identifier'),
            'fullname': user.get_contact_info('fullname'),
            'email': user.get_contact_info('email'),
        }),
        http.HTTPStatus.OK,  # 200
    )


@bp.route('/execution', methods=['GET'])
@pagination
def execution_list():
    dict_args = request.args.to_dict()

    # format query
    exe_query = dict(
        (k, format_query(v)) for k, v in dict_args.items()
        if k not in flask.current_app.config['INVALID_FILTERS']
    )

    # sort
    srt = {'started_at': -1}
    sort_query = exe_query.pop('sort', None)
    if sort_query and sort_query.split(',', 1)[0]:
        try:
            key, order = sort_query.split(',', 1)
        except ValueError:
            key, order = sort_query, 'ASCENDING'

        if order not in ['ASCENDING', 'DESCENDING']:
            order = 'ASCENDING'

        order = getattr(pymongo, order)
        srt = {key: order}

    # filter for user_identifier
    user_identifier = exe_query.pop('user_identifier', None)
    if user_identifier is not None:
        user = User.get_by('identifier', user_identifier)
        if user is not None:
            execution_list = [item.id for item in user.activities.all()]
        else:
            execution_list = []
        exe_query['id'] = {
            '$in': execution_list,
        }

    # filter for exclude/include
    exclude_fields = exe_query.pop('exclude', '')
    exclude_list = [s.strip() for s in exclude_fields.split(',') if s]
    exclude_map = {item: 0 for item in exclude_list}

    include_fields = exe_query.pop('include', '')
    include_list = [s.strip() for s in include_fields.split(',') if s]
    include_map = {item: 1 for item in include_list}

    # store project for future use
    prjct = {**include_map} or {**exclude_map}

    exe_collection = mongo.db[flask.current_app.config['EXECUTION_COLLECTION']]

    try:
        cursor_count = exe_collection.count_documents(exe_query)
        cursor = exe_collection.find(
            exe_query,
            prjct or None,
        ).sort(list(srt.items()))
    except pymongo.errors.OperationFailure:
        flask.abort(400, 'Malformed query')

    return jsonify({
        'total_count': cursor_count,
        'data': list(map(
            json_prepare,
            cursor.skip(g.offset).limit(g.limit),
        ))
    })


@bp.route('/execution/search', methods=['POST'])
@requires_auth
@requires_json
@pagination
def execution_list_search():
    dict_args = flask.request.get_json()

    # format query
    exe_query = dict(
        (k, v) for k, v in dict_args.items()
        if k not in flask.current_app.config['INVALID_FILTERS']
    )

    # sort
    srt = {'started_at': -1}
    sort_query = exe_query.pop('sort', None)
    if sort_query and sort_query.split(',', 1)[0]:
        try:
            key, order = sort_query.split(',', 1)
        except ValueError:
            key, order = sort_query, 'ASCENDING'

        if order not in ['ASCENDING', 'DESCENDING']:
            order = 'ASCENDING'

        order = getattr(pymongo, order)
        srt = {key: order}

    # filter for user_identifier
    user_identifier = exe_query.pop('user_identifier', None)
    if user_identifier is not None:
        user = User.get_by('identifier', user_identifier)
        if user is not None:
            execution_list = [item.id for item in user.activities.all()]
        else:
            execution_list = []
        exe_query['id'] = {
            '$in': execution_list,
        }

    # filter for exclude/include
    exclude_list = exe_query.pop('exclude', None) or []
    exclude_map = {item: 0 for item in exclude_list}

    include_list = exe_query.pop('include', None) or []
    include_map = {item: 1 for item in include_list}

    # store project for future use
    prjct = {**include_map} or {**exclude_map}

    exe_collection = mongo.db[flask.current_app.config['EXECUTION_COLLECTION']]

    try:
        cursor_count = exe_collection.count_documents(exe_query)
        cursor = exe_collection.find(
            exe_query,
            prjct or None,
        ).sort(list(srt.items()))
    except pymongo.errors.OperationFailure:
        flask.abort(400, 'Malformed query')

    return {
        'total_count': cursor_count,
        'executions': list(map(
            json_prepare,
            cursor.skip(g.offset).limit(g.limit),
        ))
    }, 200


@bp.route('/execution/<id>', methods=['GET'])
def process_status(id):
    collection = mongo.db[flask.current_app.config['EXECUTION_COLLECTION']]

    try:
        exc = next(collection.find({'id': id}))
    except StopIteration:
        raise ModelNotFoundError(
            'Specified execution never existed, and never will'
        )

    return jsonify({
        'data': json_prepare(exc),
    })


@bp.route('/execution/<id>', methods=['PATCH'])
@requires_auth
def execution_patch(id):
    execution = Execution.get_or_exception(id)

    collection = mongo.db[flask.current_app.config['EXECUTION_COLLECTION']]
    execution_state = next(collection.find({'id': id}))

    validate_json(request.json, ['comment', 'inputs'])

    xml = Xml.load(flask.current_app.config, execution.process_name, direct=True)
    dom = xml.get_dom()

    if type(request.json['inputs']) != list:
        raise RequiredListError('inputs', 'request.body.inputs')

    processed_inputs = []

    for i, field in enumerate(request.json['inputs']):
        if type(field) != dict:
            raise RequiredDictError(str(i), 'request.body.inputs.{}'.format(i))

        if 'ref' not in field:
            raise RequiredInputError('id',
                                     'request.body.inputs.{}.ref'.format(i))

        if type(field['ref']) != str:
            raise RequiredStrError('ref',
                                   'request.body.inputs.{}.ref'.format(i))

        # check down the state tree for existence of the requested ref
        processed_ref = []
        pieces = field['ref'].split('.')

        try:
            node_id = pieces.pop(0)
            node_state = execution_state['state']['items'][node_id]
        except IndexError:
            raise InputError(
                'Missing segment in ref for node_id',
                'request.body.inputs.{}.ref'.format(i),
                'validation.invalid')
        except KeyError:
            raise InputError(
                'node {} not found'.format(node_id),
                'request.body.inputs.{}.ref'.format(i),
                'validation.invalid')

        if node_state['type'] != 'action':
            raise InputError(
                'only action nodes may be patched',
                'request.body.inputs.{}.ref'.format(i),
                'validation.invalid')

        processed_ref.append(node_id)

        # node xml element
        node = get_element_by(dom, 'action', 'id', node_id)

        if len(node_state['actors']['items']) == 1:
            only_key = list(node_state['actors']['items'].keys())[0]
            actor_state = node_state['actors']['items'][only_key]
        else:
            try:
                actor_username = pieces.pop(0)
                actor_state = node_state['actors']['items'][actor_username]
            except IndexError:
                raise InputError(
                    'Missing segment in ref for actor username',
                    'request.body.inputs.{}.ref'.format(i),
                    'validation.invalid')
            except KeyError:
                raise InputError(
                    'actor {} not found'.format(actor_username),
                    'request.body.inputs.{}.ref'.format(i),
                    'validation.invalid')

        processed_ref.append(actor_state['user']['identifier'])

        try:
            form_ref = pieces.pop(0)
        except IndexError:
            raise InputError(
                'Missing segment in ref for form ref',
                'request.body.inputs.{}.ref'.format(i),
                'validation.invalid')

        if re.match(r'\d+', form_ref):
            try:
                form_index = int(form_ref)
                form_state = actor_state['forms'][form_index]
            except KeyError:
                raise InputError(
                    'form index {} not found'.format(form_ref),
                    'request.body.inputs.{}.ref'.format(i),
                    'validation.invalid')
        else:
            matching_forms = list(map(
                lambda f: f['ref'] == form_ref,
                actor_state['forms']
            ))
            form_count = len(list(filter(lambda x: x, matching_forms)))

            if form_count == 1:
                form_index = matching_forms.index(True)
                form_state = actor_state['forms'][form_index]
            elif form_count == 0:
                raise InputError(
                    'No forms with ref {} in node'.format(form_ref),
                    'request.body.inputs.{}.ref'.format(i),
                    'validation.invalid'
                )
            elif len(pieces) and re.match(r'\d+', pieces[0]):
                try:
                    form_n = int(pieces.pop(0))
                    # get index of the n-th matched form
                    form_index = list(filter(
                        lambda x: x[1],
                        enumerate(matching_forms),
                    ))[form_n][0]  # raise error if there is no n-th form
                    form_state = actor_state['forms'][form_index]
                except IndexError:
                    raise InputError(
                        'form index {} not found'.format(form_ref),
                        'request.body.inputs.{}.ref'.format(i),
                        'validation.invalid')
            else:
                raise InputError(
                    'More than one form with ref {}'.format(form_ref),
                    'request.body.inputs.{}.ref'.format(i),
                    'validation.invalid'
                )

        processed_ref.append(str(form_index) + ':' + form_state['ref'])

        # form xml element
        form = get_element_by(node, 'form', 'id', form_state['ref'])

        try:
            input_name = pieces.pop(0)
            form_state['inputs']['items'][input_name]
        except IndexError:
            raise InputError(
                'Missing segment in ref for input name',
                'request.body.inputs.{}.ref'.format(i),
                'validation.invalid')
        except KeyError:
            raise InputError(
                'input {} not found'.format(input_name),
                'request.body.inputs.{}.ref'.format(i),
                'validation.invalid'
            )

        processed_ref.append(input_name)

        processed_inputs.append({
            'ref': '.'.join(processed_ref),
        })

        # input xml element
        input_el = get_element_by(form, 'input', 'name', input_name)

        if 'value' in field:
            try:
                input_obj = make_input(input_el)
                value = input_obj.validate(field['value'], 0)
                caption = input_obj.make_caption(value)

                processed_inputs[-1]['value'] = value
                processed_inputs[-1]['value_caption'] = caption
            except InputError as e:
                raise InputError(
                    'value invalid: {}'.format(str(e)),
                    'request.body.inputs.{}.value'.format(i),
                    'validation.invalid')

    handle.delay(json.dumps({
        'command': 'patch',
        'execution_id': execution.id,
        'comment': request.json['comment'],
        'inputs': processed_inputs,
        'user_identifier': g.user.identifier,
    }))
    sse.publish(**{
        'data': {"execution_id": execution.id},
        'type': 'execution_patch',
    })

    return jsonify({
        'data': 'accepted',
    }), 202


@bp.route('/execution/<exe_id>/user', methods=['POST'])
@requires_auth
def execution_add_user(exe_id):
    ''' adds the user as a candidate for solving the given node, only if the
    node has an active pointer. '''
    # TODO possible race condition introduced here. How does this code work in
    # case the handler is moving the pointer?

    # get execution
    execution = Execution.get_or_exception(exe_id)

    # validate the members needed
    validate_json(request.json, ['identifier', 'node_id'])

    identifier = request.json['identifier']
    node_id = request.json['node_id']

    # get actual pointer
    try:
        pointer = next(execution.pointers.q().filter(node_id=node_id))
    except StopIteration:
        raise BadRequest([{
            'detail': f'{node_id} does not have a live pointer',
            'code': 'validation.no_live_pointer',
            'where': 'request.body.node_id',
        }])

    # get user
    user = User.get_by('identifier', identifier)
    if user is None:
        raise InvalidInputError('user_id', 'request.body.identifier')

    # update user
    user.tasks.add(pointer)

    user_json = user.to_json()

    # update pointer
    ptr_collection = mongo.db[flask.current_app.config['POINTER_COLLECTION']]
    ptr = ptr_collection.find_one({
        'execution.id': exe_id,
        'id': pointer.id,
        'node.id': node_id,
        'state': 'ongoing',
    })

    if not ptr:
        raise BadRequest([{
            'detail': f'{node_id} does not have a live pointer',
            'code': 'validation.no_live_pointer',
            'where': 'request.body.node_id',
        }])

    if user_json['identifier'] not in [
        x['identifier'] for x in ptr['notified_users']
    ]:
        ptr['notified_users'].append(user_json)

    ptr_collection.update_one(
        {
            'execution.id': exe_id,
            'id': pointer.id,
            'node.id': node_id,
            'state': 'ongoing',
        },
        {'$set': {'notified_users': ptr['notified_users']}},
    )

    return jsonify(user_json), 200


@bp.route('/execution/<id>', methods=['DELETE'])
@requires_auth
def delete_process(id):
    execution = Execution.get_or_exception(id)

    handle.delay(json.dumps({
        'command': 'cancel',
        'execution_id': execution.id,
    }))
    sse.publish(**{
        'data': {"execution_id": execution.id},
        'type': 'execution_delete',
    })

    return jsonify({
        'data': 'accepted',
    }), 202


@bp.route('/execution', methods=['POST'])
@requires_auth
@requires_json
def start_process():
    validate_json(request.json, ['process_name'])

    try:
        xml = Xml.load(flask.current_app.config, request.json['process_name'])
    except ProcessNotFound:
        raise NotFound([{
            'detail': '{} process does not exist'
                      .format(request.json['process_name']),
            'where': 'request.body.process_name',
        }])
    except MalformedProcess as e:
        raise UnprocessableEntity([{
            'detail': str(e),
            'where': 'request.body.process_name',
        }])

    xmliter = iter(xml)
    node = make_node(next(xmliter), xmliter)

    # Check for authorization
    validate_auth(node, g.user)

    # check if there are any forms present
    input = node.validate_input(request.json)

    # get rabbit channel for process queue
    execution = xml.start(node, input, mongo.db, g.user.identifier)
    sse.publish(**{
        'data': {"execution_id": execution.id},
        'type': 'execution_create',
    })

    return {
        'data': execution.to_json(),
    }, 201


@bp.route('/pointer', methods=['POST'])
@requires_auth
@requires_json
def continue_process():
    validate_json(request.json, ['execution_id', 'node_id'])

    execution_id = request.json['execution_id']
    node_id = request.json['node_id']

    try:
        execution = Execution.get_or_exception(execution_id)
    except ModelNotFoundError:
        raise BadRequest([{
            'detail': 'execution_id is not valid',
            'code': 'validation.invalid',
            'where': 'request.body.execution_id',
        }])

    xml = Xml.load(flask.current_app.config, execution.process_name, direct=True)
    xmliter = iter(xml)

    collection = mongo.db[flask.current_app.config['EXECUTION_COLLECTION']]
    state = collection.find_one({
        'id': execution.id,
    }) or {}

    try:
        continue_point = make_node(
            xmliter.find(lambda e: e.getAttribute('id') == node_id),
            xmliter,
            context=make_context(state, {}),
        )
    except ElementNotFound:
        raise BadRequest([{
            'detail': 'node_id is not a valid node',
            'code': 'validation.invalid_node',
            'where': 'request.body.node_id',
        }])

    try:
        pointer = next(execution.pointers.q().filter(node_id=node_id))
    except StopIteration:
        raise BadRequest([{
            'detail': 'node_id does not have a live pointer',
            'code': 'validation.no_live_pointer',
            'where': 'request.body.node_id',
        }])

    # Check for authorization
    if pointer not in g.user.tasks:
        raise Forbidden([{
            'detail': 'Provided user does not have this task assigned',
            'where': 'request.authorization',
        }])

    # Validate asociated forms
    collected_input = continue_point.validate_input(request.json)

    # trigger rabbit
    handle.delay(json.dumps({
        'command': 'step',
        'pointer_id': pointer.id,
        'user_identifier': g.user.identifier,
        'input': collected_input,
    }))
    sse.publish(**{
        'data': {"execution_id": execution.id},
        'type': 'execution_update',
    })

    return {
        'data': 'accepted',
    }, 202


@bp.route('/pointer/<id>', methods=['GET'])
def read_pointer(id):
    collection = mongo.db[flask.current_app.config['POINTER_COLLECTION']]
    query = {'id': id}

    return jsonify({
        "data": json_prepare(
            collection.find_one(query)
        ),
    })


@bp.route('/pointer', methods=['GET'])
@pagination
def fetch_pointers():
    dict_args = request.args.to_dict()

    # format query
    ptr_query = dict(
        (k, format_query(v)) for k, v in dict_args.items()
        if k not in flask.current_app.config['INVALID_FILTERS']
    )

    # sort
    srt = {'started_at': -1}
    sort_query = ptr_query.pop('sort', None)
    if sort_query and sort_query.split(',', 1)[0]:
        try:
            key, order = sort_query.split(',', 1)
        except ValueError:
            key, order = sort_query, 'ASCENDING'

        if order not in ['ASCENDING', 'DESCENDING']:
            order = 'ASCENDING'

        order = getattr(pymongo, order)
        srt = {key: order}

    # filter for user_identifier
    user_identifier = ptr_query.pop('user_identifier', None)
    if user_identifier is not None:
        user = User.get_by('identifier', user_identifier)
        if user is not None:
            pointer_list = [item.id for item in user.tasks.all()]
        else:
            pointer_list = []
        ptr_query['id'] = {
            '$in': pointer_list,
        }

    # filter for exclude/include
    exclude_fields = ptr_query.pop('exclude', '')
    exclude_list = [s.strip() for s in exclude_fields.split(',') if s]
    exclude_map = {item: 0 for item in exclude_list}

    include_fields = ptr_query.pop('include', '')
    include_list = [s.strip() for s in include_fields.split(',') if s]
    include_map = {item: 1 for item in include_list}

    # store project for future use
    prjct = {**include_map} or {**exclude_map}

    ptr_collection = mongo.db[flask.current_app.config['POINTER_COLLECTION']]

    try:
        cursor_count = ptr_collection.count_documents(ptr_query)
        cursor = ptr_collection.find(
            ptr_query,
            prjct or None,
        ).sort(list(srt.items()))
    except pymongo.errors.OperationFailure:
        flask.abort(400, 'Malformed query')

    return jsonify({
        'total_count': cursor_count,
        'pointers': list(map(
            json_prepare,
            cursor.skip(g.offset).limit(g.limit),
        ))
    })


@bp.route('/pointer/search', methods=['POST'])
@requires_auth
@requires_json
@pagination
def pointer_list_search():
    dict_args = flask.request.get_json()

    # format query
    ptr_query = dict(
        (k, v) for k, v in dict_args.items()
        if k not in flask.current_app.config['INVALID_FILTERS']
    )

    # sort
    srt = {'started_at': -1}
    sort_query = ptr_query.pop('sort', None)
    if sort_query and sort_query.split(',', 1)[0]:
        try:
            key, order = sort_query.split(',', 1)
        except ValueError:
            key, order = sort_query, 'ASCENDING'

        if order not in ['ASCENDING', 'DESCENDING']:
            order = 'ASCENDING'

        order = getattr(pymongo, order)
        srt = {key: order}

    # filter for user_identifier
    user_identifier = ptr_query.pop('user_identifier', None)
    if user_identifier is not None:
        user = User.get_by('identifier', user_identifier)
        if user is not None:
            pointer_list = [item.id for item in user.tasks.all()]
        else:
            pointer_list = []
        ptr_query['id'] = {
            '$in': pointer_list,
        }

    # filter for exclude/include
    exclude_list = ptr_query.pop('exclude', None) or []
    exclude_map = {item: 0 for item in exclude_list}

    include_list = ptr_query.pop('include', None) or []
    include_map = {item: 1 for item in include_list}

    # store project for future use
    prjct = {**include_map} or {**exclude_map}

    ptr_collection = mongo.db[flask.current_app.config['POINTER_COLLECTION']]

    try:
        cursor_count = ptr_collection.count_documents(ptr_query)
        cursor = ptr_collection.find(
            ptr_query,
            prjct or None,
        ).sort(list(srt.items()))
    except pymongo.errors.OperationFailure:
        flask.abort(400, 'Malformed query')

    return {
        'total_count': cursor_count,
        'pointers': list(map(
            json_prepare,
            cursor.skip(g.offset).limit(g.limit),
        ))
    }, 200


@bp.route('/process', methods=['GET'])
def list_process():
    def add_form(xml):
        json_xml = xml.to_json()
        forms = []
        xmliter = iter(xml)
        first_node = next(xmliter)
        xmliter.parser.expandNode(first_node)

        for form in first_node.getElementsByTagName('form'):
            forms.append(form_to_dict(form))

        json_xml['form_array'] = forms

        return json_xml

    return jsonify({
        'data': list(filter(
            lambda x: x,
            map(
                add_form,
                Xml.list(flask.current_app.config),
            )
        )),
    })


@bp.route('/process/<name>', methods=['GET'])
def find_process(name):
    def add_form(xml):
        json_xml = xml.to_json()
        forms = []
        xmliter = iter(xml)
        first_node = next(xmliter)
        xmliter.parser.expandNode(first_node)

        for form in first_node.getElementsByTagName('form'):
            forms.append(form_to_dict(form))

        json_xml['form_array'] = forms

        return json_xml

    version = request.args.get('version', '')

    if version:
        version = ".{}".format(version)

    process_name = "{}{}".format(name, version)

    try:
        xml = Xml.load(flask.current_app.config, process_name)
    except ProcessNotFound:
        raise NotFound([{
            'detail': '{} process does not exist'
                      .format(process_name),
            'where': 'request.body.process_name',
        }])

    return jsonify({
        'data': add_form(xml),
    })


@bp.route('/process/<name>.xml', methods=['GET'])
def xml_process(name):
    version = request.args.get('version', '')

    if version:
        version = ".{}".format(version)

    process_name = "{}{}".format(name, version)

    try:
        xml = Xml.load(flask.current_app.config, process_name)
    except ProcessNotFound:
        raise NotFound([{
            'detail': '{} process does not exist'
                      .format(process_name),
            'where': 'request.body.process_name',
        }])
    ruta = os.path.join(flask.current_app.config['XML_PATH'], xml.filename)
    return open(ruta).read(), {'Content-Type': 'text/xml; charset=utf-8'}


@bp.route('/activity', methods=['GET'])
@requires_auth
def list_activities():
    activities = g.user.activities.all()

    return jsonify({
        'data': list(map(
            lambda a: a.to_json(include=['*', 'execution']),
            activities
        )),
    })


@bp.route('/task', methods=['GET'])
@requires_auth
def task_list():
    tasks = g.user.tasks.all()

    return jsonify({
        'data': list(map(
            lambda t: t.to_json(include=['*', 'execution']),
            tasks
        )),
    })


@bp.route('/task/<id>', methods=['GET'])
@requires_auth
def task_read(id):
    pointer = Pointer.get_or_exception(id)

    if pointer not in g.user.tasks:
        raise Forbidden([{
            'detail': 'Provided user does not have this task assigned',
            'where': 'request.authorization',
        }])

    execution = pointer.execution.get()
    collection = mongo.db[flask.current_app.config['EXECUTION_COLLECTION']]
    state = collection.find_one({
        'id': execution.id,
    })

    xml = Xml.load(
        flask.current_app.config,
        execution.process_name,
        direct=True
    )
    xmliter = iter(xml)
    node = xmliter.find(lambda e: e.getAttribute('id') == pointer.node_id)

    xmliter.parser.expandNode(node)

    # Response body
    json_data = pointer.to_json(include=['*', 'execution'])

    # Append node info
    json_data['node_type'] = node.tagName

    context = make_context(state, {})

    # Append forms
    forms = []
    for form in node.getElementsByTagName('form'):
        forms.append(form_to_dict(form, context=context))
    json_data['form_array'] = forms

    # If any append previous work done
    node_state = state['state']['items'][pointer.node_id]
    node_actors = node_state['actors']

    user_identifier = g.user.identifier
    if user_identifier in node_actors['items']:
        action = node_actors['items'][user_identifier]

        json_data['prev_work'] = action['forms']

    # Append validation
    if node.tagName == 'validation':
        deps = list(map(
            lambda node: get_text(node),
            node.getElementsByTagName('dep')
        ))

        fields = []
        for dep in deps:
            form_ref, input_name = dep.split('.')

            # TODO this could be done in O(log N + K)
            for node in state['state']['items'].values():
                if node['state'] != 'valid':
                    continue

                for identifier in node['actors']['items']:
                    actor = node['actors']['items'][identifier]
                    if actor['state'] != 'valid':
                        continue

                    for form_ix, form in enumerate(actor['forms']):
                        if form['state'] != 'valid':
                            continue

                        if form['ref'] != form_ref:
                            continue

                        if input_name not in form['inputs']['items']:
                            continue

                        input = form['inputs']['items'][input_name]

                        state_ref = [
                            node['id'],
                            identifier,
                            str(form_ix),
                        ]
                        state_ref = '.'.join(state_ref)
                        state_ref = state_ref + ':' + dep

                        field = {
                            'ref': state_ref,
                            **input,
                        }
                        del field['state']

                        fields.append(field)

        json_data['fields'] = fields

    return jsonify({
        'data': json_data,
    })


@bp.route('/log', methods=['GET'])
@pagination
def all_logs():
    collection = mongo.db[flask.current_app.config['POINTER_COLLECTION']]

    dict_args = request.args.to_dict()

    query = dict(
        (k, dict_args[k]) for k in dict_args
        if k not in flask.current_app.config['INVALID_FILTERS']
    )

    # filter for user_identifier
    user_identifier = query.pop('user_identifier', None)
    if user_identifier is not None:
        user = User.get_by('identifier', user_identifier)
        if user is not None:
            pointer_list = [item.id for item in user.tasks.all()]
        else:
            pointer_list = []
        query['id'] = {
            '$in': pointer_list,
        }

    pipeline = [
        {'$match': query},
        {'$sort': {'started_at': -1}},
        {'$group': {
            '_id': '$execution.id',
            'latest': {'$first': '$$ROOT'},
        }},
        {'$replaceRoot': {'newRoot': '$latest'}},
        {'$sort': {'started_at': -1}},
        {'$skip': g.offset},
        {'$limit': g.limit},
    ]

    return jsonify({
        'data': list(map(
            json_prepare,
            collection.aggregate(pipeline),
        )),
    })


@bp.route('/log/<id>', methods=['GET'])
@pagination
def list_logs(id):
    collection = mongo.db[flask.current_app.config['POINTER_COLLECTION']]
    node_id = request.args.get('node_id')
    query = {'execution.id': id}

    if node_id:
        query['node.id'] = node_id

    return jsonify({
        "data": list(map(
            json_prepare,
            collection.find(query).skip(g.offset).limit(g.limit).sort([
                ('started_at', pymongo.DESCENDING)
            ])
        )),
    })


@bp.route('/process/<id>/statistics', methods=['GET'])
def node_statistics(id):
    collection = mongo.db[flask.current_app.config['POINTER_COLLECTION']]
    query = [
        {"$match": {"process_id": id}},
        {"$project": {
            "process_id": "$process_id",
            "node": "$node.id",
            "difference_time": {
                "$subtract": ["$finished_at", "$started_at"],
            },
        }},
        {"$group": {
            "_id": {"process_id": "$process_id", "node": "$node"},
            "process_id": {"$first": "$process_id"},
            "node": {"$first": "$node"},
            "max": {
                "$max": {
                    "$divide": ["$difference_time", 1000],
                },
            },
            "min": {
                "$min": {
                    "$divide": ["$difference_time", 1000],
                },
            },
            "average": {
                "$avg": {
                    "$divide": ["$difference_time", 1000],
                },
            },
        }},

        {"$sort": {"execution": 1, "node": 1}}
    ]
    return jsonify({
        "data": list(map(
            json_prepare,
            collection.aggregate(query)
        )),
    })


@bp.route('/process/statistics', methods=['GET'])
@pagination
def process_statistics():
    collection = mongo.db[flask.current_app.config['EXECUTION_COLLECTION']]
    query = [
        {"$match": {"status": "finished"}},
        {"$skip": g.offset},
        {"$limit": g.limit},
        {"$project": {
            "difference_time": {
                "$subtract": ["$finished_at", "$started_at"],
            },
            "process":{"id": "$process.id"},
        }},

        {"$group": {
            "_id": "$process.id",
            "process": {"$first": "$process.id"},
            "max": {
                "$max": {
                    "$divide": ["$difference_time", 1000],
                },
            },
            "min": {
                "$min": {
                    "$divide": ["$difference_time", 1000],
                },
            },
            "average": {
                "$avg": {
                    "$divide": ["$difference_time", 1000],
                },
            },

        }},
        {"$sort": {"process": 1}},
    ]

    return jsonify({
        "data": list(map(
            json_prepare,
            collection.aggregate(query)
        )),
    })
