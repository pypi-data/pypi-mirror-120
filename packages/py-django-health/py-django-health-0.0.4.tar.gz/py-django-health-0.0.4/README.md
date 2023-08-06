# Health Checkers
#### For `django` applications.

## Installation
> pip install py-django-health

## Usage
In `settings.py` file:
```python
INSTALLED_APPS = [
    'health',
    ...
]
```

## Using checkers
By default, you have 3 checkers set (which are the built-in defined by the library):
- `health.checkers.disk.DiskHealthChecker`
- `health.checkers.database.DatabaseHealthChecker`
- `health.checkers.cache.CacheHealthChecker`

If you want to replace them or use another, just modify this property in the `settings.py` file:
```python
HEALTH_CHECKERS = {
    'health.checkers.disk.DiskHealthChecker',
    ...
}
```
Remember: `HEALTH_CHECKERS` is a set of strings.

## Exposing endpoints
Health Checkers has endpoints to be consumed by others apps or metrics counters.  
To enabled them, just add them into your `urls.py` file:
```python
url('', include('health.urls'))
```

## Configuring the application
### HEALTH_CHECKERS_ENABLED
| Type | Required | Default | 
| --- | --- | --- |
| bool | No | `True` |
> Enable or disabled all health checker features.

### HEALTH_CHECKERS
| Type | Required | Default | 
| --- | --- | --- |
| set | No | `{'health.checkers.disk.DiskHealthChecker', 'health.checkers.database.DatabaseHealthChecker', 'health.checkers.cache.CacheHealthChecker'}` |
> Set of checkers to execute

### HEALTH_CHECKERS_CONTEXT_PATH
| Type | Required | Default | 
| --- | --- | --- |
| str | No | `/infra` |
> Context path for exposed endpoint

## Adding custom checkers
You can create and add custom checkers.  
Just follow these steps:
1. Create a class inheriting the class `HealthChecker` from the package _health.checkers.base_.
```python
from health.checkers.base import HealthChecker

class MyCustomChecker(HealthChecker):
    _token: str
```
2. Override (if needed) the `setup` method.
```python
import typing

from health.checkers.base import HealthChecker

class MyCustomChecker(HealthChecker):
    _token: str
    
    def setup(self) -> typing.NoReturn:
        self._token = '<token>'
```
3. Override the `check` method.
```python
import typing

from health.checkers.base import HealthChecker
from health.models import ComponentHealth

class MyCustomChecker(HealthChecker):
    _token: str
    
    def setup(self) -> typing.NoReturn:         
        self._token = '<token>'
        
    def check(self) -> typing.List[ComponentHealth]:       
       # Logic goes here 
       return []
```
4. Add the custom checker into the `HEALTH_CHECKERS` set into the `settings.py` file.
```python
HEALTH_CHECKERS = {
   'health.checkers.disk.DiskHealthChecker',
   'health.checkers.database.DatabaseHealthChecker',
   'my_package.checkers.MyCustomChecker'
}
```
5. You can also create a new `ComponentHealth`.
```python
from health.models import ComponentHealth

class MyCustomHealthComponent(ComponentHealth):
    token: str
```

## Consuming endpoint 
### Get Health information
> Retrieve health information from the application.

| Method | Path | 
| --- | --- |
| `GET` | `/{HEALTH_CHECKERS_CONTEXT_PATH}/health` |

Response (JSON): 
````json
{
   "status": "ALIVE",
   "components": [
      {
         "type": "DISK",
         "status": "ALIVE",
         "total": 50699194432,
         "free": 5131434234,
         "used": 4551234 
      }
   ]
}
````


