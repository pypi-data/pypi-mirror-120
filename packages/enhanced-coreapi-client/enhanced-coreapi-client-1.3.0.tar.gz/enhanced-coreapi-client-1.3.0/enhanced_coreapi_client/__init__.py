from __future__ import unicode_literals, absolute_import

import coreapi


class Client(object):

    client = None
    schema = None
    _url = None
    _keys = []

    def __init__(self, url, keys=[], client=None, schema=None, **kwargs):

        if not client:
            client = coreapi.Client(**kwargs)
        if not schema:
            schema = client.get(url)

        self.client = client
        self.schema = schema
        self._url = url
        self._keys = keys

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

        return self.__class__(
            self._url,
            self._keys + [key],
            self.client,
            self.schema,
        )

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        return self.action(self._keys, **kwargs)

    def action(self, keys, **kwargs):
        return self.client.action(self.schema, keys, params=kwargs)
