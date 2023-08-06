import requests

from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.status import is_success
from abc import ABC
from contextlib import suppress
from simplejson import JSONDecodeError


class AbstractServiceProvider(ABC):
    default_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.host = None
        self.headers = self.default_headers

    def create_request(self, method: str, **kwargs):
        """
        Make a request but return response instance
        :param method:
        :param kwargs:
        :return:
        """
        url = kwargs.pop('url')
        params = {'url': f'{self.host}{url}', 'headers': self.headers}
        params.update(kwargs)

        # Where requests is a package, method are 'get' or 'post'
        response = getattr(requests, method)(**params)

        if not is_success(response.status_code):
            detail = {}
            validation = ValidationError(detail=detail, code=response.status_code)

            with suppress(JSONDecodeError):
                validation.detail.update(**response.json())
                raise validation

            validation.detail = {
                'code': response.status_code,
                'detail': _('Remote provider failure.'),
                'content_type': response.headers['content-type'],
                'content': response.content,
            }

            raise validation

        return response

    def make_request(self, method: str, **kwargs):
        """
        Make a request but return json
        :param method:
        :param kwargs:
        :return:
        """
        response = self.create_request(method, **kwargs)
        return response.json()
