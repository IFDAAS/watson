# -*- coding: utf-8 -*-
import re
from watson.di import ContainerAware
from watson.http.messages import Response, Request
from watson.stdlib.imports import get_qualified_name


class BaseController(ContainerAware):
    def execute(self, **kwargs):
        raise NotImplementedError('You must implement execute')

    def get_execute_method_path(self, **kwargs):
        raise NotImplementedError('You must implement get_execute_method_path')

    def __repr__(self):
        return '<{0}>'.format(get_qualified_name(self))


class BaseHttpController(BaseController):
    _request = None
    _response = None

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request):
        if not isinstance(request, Request):
            raise TypeError('Invalid request type, expected watson.http.messages.Request')
        self._request = request

    @property
    def response(self):
        if not self._response:
            self.response = Response()
        return self._response

    @response.setter
    def response(self, response):
        if not isinstance(response, Response):
            raise TypeError('Invalid response type, expected watson.http.messages.Response')
        self._response = response

    # todo redirect


class ActionController(BaseHttpController):
    def execute(self, **kwargs):
        method = getattr(self, kwargs.get('action', 'index') + '_action')
        try:
            result = method(**kwargs)
        except TypeError:
            result = method()
        return result

    def get_execute_method_path(self, **kwargs):
        return [self.__class__.__name__.lower(),
                re.sub('.-', '_', kwargs.get('action', 'index').lower())]


class RestController(BaseHttpController):
    def execute(self, **kwargs):
        method = getattr(self, self.request.method)
        try:
            result = method(**kwargs)
        except TypeError:
            result = method()
        return result

    def get_execute_method_path(self, **kwargs):
        return [self.__class__.__name__.lower(), self.request.method.lower()]
