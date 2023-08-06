#######################
Enhanced CoreAPI client
#######################

Wrapper around ``coreapi.Client`` for more convenient usage.

#####
Usage
#####

Initialize client:

.. code-block:: python

    from enhanced_coreapi_client import Client
    conf = {
        'SCHEMA_URL': 'https://example.com/api/schema/',
        'AUTH_USERNAME': 'client-example',
        'AUTH_PASSWORD': 'password-example',
    }
   client = Client(conf)


Access API endpoints in accordance with the schema, e.g.:

.. code-block:: python

   users = client.api.users.list()
   project = client.api.users.projects.read(id=7)
   new_project = client.api.users.projects.create(name='xxx', user_id=3)
