import json
import datetime
from collections import namedtuple
from contextlib import contextmanager

import responses
from nose.tools import raises

from mondo import MondoClient

Response = namedtuple('Response', ['method', 'url', 'body', 'status', 'content_type'])


ACCOUNT_ID = 'account_id'


MONDO_RESPONSES = {
    'failed_oauth2': Response(
        responses.POST,
        'https://api.getmondo.co.uk/oauth2/token',
        json.dumps({
            'error': 'not found',
        }),
        404,
        'application/json'
    ),
    'success_oauth2': Response(
        responses.POST,
        'https://api.getmondo.co.uk/oauth2/token',
        json.dumps({
            'access_token': 'access_token_here',
            'refresh_token': 'refresh_token_here',
            'expires_in': 10
        }),
        200,
        'application/json'
    )
}


@contextmanager
def load_response(name):
    responses.add(**MONDO_RESPONSES.get(name)._asdict())
    yield


@responses.activate
@raises(Exception)
def test_invalid_oauth_raises_exception():
    with load_response('failed_oauth2'):
        MondoClient('', '', '', '')


@responses.activate
def test_valid_oauth_has_token_with_a_expires_time():
    with load_response('success_oauth2'):
        client = MondoClient('', '', '', '')
        assert client.token == 'access_token_here'
        assert client.refresh_token == 'refresh_token_here'
        assert isinstance(client.token_expires, datetime.datetime)
