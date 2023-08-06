import json
import jwt

from abc import ABC
from drf_util.utils import gt
from datetime import datetime, timedelta
from .abstract import AbstractServiceProvider


# Create your class here.


class StaticAPI(AbstractServiceProvider, ABC):
    # Versions
    URI_V1 = 'v1/'
    URI_V2 = 'v2/'

    # Endpoints
    URL_CREATE_APPLICATION = 'application/'
    URL_CREATE_APPLICATION_USERS = 'application/users/'

    def __init__(self, host='', silent=False):
        """
        :param host: Hostname of Static Pages API
        :param silent: Using this parameter will silent errors thrown from abstract class
        :return:
        """
        super().__init__()
        self.host = host
        self.silent = silent

    def set_host(self, host):
        self.host = host
        return self

    def set_silent(self, silent: bool):
        self.silent = silent
        return self

    def set_api_key(self, key):
        self.headers['X-API-Key'] = f'{key}'
        return self

    def set_authorization(self, token):
        self.headers['Authorization'] = f'Bearer {token}'
        return self

    def make_application(self):
        """
        Create an application
        :return:
        """
        return self.v2(method='post', endpoint=self.URL_CREATE_APPLICATION)

    def make_application_user(self, **kwargs):
        """
        Create application user or users
        :param kwargs:
        :return:
        """
        user = kwargs.get('user', None) or None
        users = kwargs.get('users', []) or []

        if isinstance(users, list) and user:
            users += [user]

        payload = {'users': users}
        return self.v2(method='post', endpoint=self.URL_CREATE_APPLICATION_USERS, data=payload)

    @staticmethod
    def make_application_user_token(**kwargs) -> str:
        """
        Create application user token
        :param kwargs:
        :return:
        """

        return jwt.encode({
            'id': gt(kwargs, 'id', ''),
            'full_name': gt(kwargs, 'full_name', ''),
            'email': gt(kwargs, 'email', ''),
            'exp': datetime.now() + timedelta(weeks=2)
        }, gt(kwargs, 'secret', ''), )

    def requester(self, version='', **kwargs):
        """
        Requests resources
        :param version:
        :param kwargs:
        :return:
        """
        method = kwargs.get('method', 'get') or 'get'
        endpoint = kwargs.get('endpoint', '') or ''
        payload = kwargs.get('data', {}) or {}

        uri = f'{version}{endpoint}'

        data = json.dumps(payload)
        params = {'url': uri, 'data': data}

        response = {}
        if self.silent:
            try:
                response = self.make_request(method=method, **params)
            except Exception as e:
                return gt(e, 'detail', {}) or {}

        if not self.silent:
            response = self.make_request(method=method, **params)

        return response

    def v1(self, **kwargs):
        """
        Requests V1 resources
        :param kwargs:
        :return:
        """
        return self.requester(version=self.URI_V1, **kwargs)

    def v2(self, **kwargs):
        """
        Requests V2 resources
        :param kwargs:
        :return:
        """
        return self.requester(version=self.URI_V2, **kwargs)
