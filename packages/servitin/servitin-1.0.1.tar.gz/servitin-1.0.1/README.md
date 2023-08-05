# About
This package provides services for django applications. The servitin service is an asynchronous standalone application.

"... when covid times came, Django walked past the pharmacy and saw a package of pills on which it was written: "
```
Servitin anti COVID pills!

stay home 50mg
code 50mg
```


# Installation
```shell
pip install servitin
```

# Howto

Make sure you have ```LOGGING``` settings in your project - servitin needs this.

Let's say you have a django ```myapp```. Make sure it is enabled in the Django settings.

Make ```myapp``` a servitin service by adding the line ```is_servitin = True``` in ```myapp/apps.py```:
```python
from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    is_servitin = True
```

Create file ```myapp/servitin.py```:

```python
from servitin.base import BaseService

class Service(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info(f"Myapp service ready.")
```

Create file ```myapp/settings.py```.

(Not necessary) Give the version ```myapp```, write in the file ```myapp/__init__.py```:
```python
__version__ = '1.0'
```

Start service:
```shell
./manage.py run_servitin
```

If all is ok you will see in the log ```Myapp service ready.```

# Request handling
Edit ```myapp/servitin.py``` to make the service as the ZeroMQ server:

```python
from servitin.base import BaseService
from servitin.lib.zmq.server import ZMQServer

class Service(ZMQServer, BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info(f"Myapp service ready.")
```

Add to ```myapp/settings.py```:

```python
from django.conf import settings

settings.SERVITIN_MYAPP_ZMQ = getattr(settings, 'SERVITIN_MYAPP_ZMQ', {
    'HOST': 'tcp://127.0.0.1',  # or 0.0.0.0 for speak to world
    'PORT': 55555,
    'SECRET': '',  # connection password
    'CRYPTO_ALGORITHM': 'HS256'
})
```

Create file ```myapp/zmq.py```:

```python
from servitin.lib.zmq.server import zmq, Response
from asgiref.sync import sync_to_async
from django.core import serializers
from django.contrib.auth.models import User
from servitin.utils import serializable

@zmq
async def get_users(request):
    order_by = request.data['order_by']
    request.log.info(f'request order: {order_by}', name='@get_users')

    def get_data():
        # data with datetime objects, so it no serializable
        data = serializers.serialize('python', User.objects.all().order_by(order_by), fields=('username', 'date_joined'))
        # so make it serializable
        return serializable(data)
    
    return Response(request, await sync_to_async(get_data)())
```

The service is ready to handle requests, let's test it.

Create django management command ```myapp/management/commands/test_myapp_service.py```:

```python
import asyncio
from django.core.management import BaseCommand
from servitin.lib.zmq.client import Servitin
import myapp.settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        service = Servitin('myapp')

        async def hello():
            print(await service.request('get_users', {'order_by': 'username'}))

        asyncio.run(hello())
        service.close()
```

Run it:
```shell
./manage.py test_myapp_service
```
