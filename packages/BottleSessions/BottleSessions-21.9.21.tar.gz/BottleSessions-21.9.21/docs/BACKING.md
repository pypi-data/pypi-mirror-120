
# Configuring Backing Store

The backing store for **BottleSessions** is the **cachelib** library from the _**Pallets**_ project.

BottleSessions `session_backing=` supports these *cachelib* classes:

* **SimpleCache:**
  * memory based 
  * single process
  * non-persistent across restarts
  * explictly select as **cache_type='SimpleCache'**
  * no required options
  * no additional packages
  * this is the default for BottleSessions

* **FileSystemCache:**
  * file-based
  * persistent
  * single host
  * select as **cache_type='FileSystem'**
  * **required:** specify **cache_dir=<_path_>**
  * no additional packages

* **RedisCache:**
  * network based
  * persistent
  * select as **cache_type= 'RedisCache'**
  * no required options (defaults use a local instance of redis)
  * rich configuration options
  * uses **redis** package

* **Memcached**
  * network based
  * persistent
  * select as **cache_type='Memcached'**
  * **required:** specify **servers=** (no default)
  * rich configuration options
  * uses **python-memcached** package


All these cache types have specific parameters available for setting ttl, prefix keys, cache expiration, *etc*. Some options are required for some cache_types. Refer to the *[cachelib documentation]( https://cachelib.readthedocs.io/en/stable/)* for full details.

To configure these options, provide more detailed configuration information when instantiating the BottleSessions class (see below).

For simple applications of light traffic, **SimpleCache** works. If state needs to be maintained longer, and accross application restarts, **FileSystem** is still pretty easy. Both are perfect during development.

For complex apps, perhaps running behind an application load balancer, or even a DNS round-robin, **RedisCache** and **Memcached** are both gold standards.

With **BottleSessions** and **cachelib**, the work involved in changing from one backing store to another is providing the cache specific initialization. The rest of the API, and hence your code, doesn't change.

Selecting a cache technology is accomplised with cache_type option e.g **cache_type='SimpleCache'**. You can provide this and module specific options as key-word arguments to **BottleSessions()**:

```python
btl = BottleSessions(app,
        cache_type='RedisCache', 
        prefix_key='XYZ', 
        host=rcache.example.org, 
        port=6379, 
        password='u2s52zodA',
        session_cookie='OREOS')
```
You can provide the options as a `dict` passed to  `session_backing=` parameter:

```python
redis_params = {
        'cache_type': 'RedisCache', 
        'host': 'localhost',
        'password': None
    }

btl = BottleSessions(app, session_backing=redis_params)
```
These can be kept in a config file - seperating configuration for the code itself.
```python
from config import backing_params, session_expire

BottleSession(app, 
    session_backing=backing_params, 
    session_expire=session_expire)
```
You can preconfigure a `BottleSessions.Backing` cache object and pass this to `session_backing=`. You can then use the session backing to cache other items in your app.
```python
from BottleSessions import BottleSessions, Backing
from config import redis_config

backing = Backing(**redis_config)
btl = BottleSession(session_backing=backing, session_expire=3600)
```

