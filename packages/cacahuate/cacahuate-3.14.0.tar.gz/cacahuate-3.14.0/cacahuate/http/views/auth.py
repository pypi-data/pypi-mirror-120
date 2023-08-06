import flask
from random import choice
from string import ascii_letters

from cacahuate.http.errors import Unauthorized
from cacahuate.models import User, Token, get_or_create_user


bp = flask.Blueprint('auth', __name__)


@bp.route('/auth/signin/<AuthProvider:backend>', methods=['POST'])
def signin(backend):
    # this raises AuthenticationError exception if failed
    identifier, data = backend.authenticate(**flask.request.form.to_dict())

    user = get_or_create_user(identifier, data)

    # creates auth token
    if user.tokens.count() > 0:
        token = user.tokens.all()[0]
    else:
        token = ''.join(choice(ascii_letters) for _ in range(32))
        token = Token(token=token).save()
        token.user.set(user)

    return flask.jsonify({
        'data': {
            'username': user.identifier,
            'fullname': user.fullname,
            'token': token.token,
        }
    })


@bp.route('/auth/whoami')
def whoami():
    identifier = flask.request.authorization['username']
    token = flask.request.authorization['password']

    user = User.get_by('identifier', identifier)
    token = Token.get_by('token', token)

    if user is None or \
       token is None or \
       token.user.get().id != user.id:
        raise Unauthorized([{
            'detail': 'Your credentials are invalid, sorry',
            'where': 'request.authorization',
        }])

    return flask.jsonify({
        'data': user.to_json(),
    })
