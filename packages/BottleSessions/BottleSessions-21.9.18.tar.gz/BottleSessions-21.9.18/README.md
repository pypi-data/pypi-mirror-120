
## BottleSessions

**BottleSessions** is middleware providing web _sessions_ for the **[Bottle](http://bottlepy.org/docs/dev/)** *micro web-framework*.  

The goal of **BottleSessions** is to provide easy to use and flexible to configure sessions. The _defaults_ attempt to make sense for typical bottle web apps with little or no tuning.  

**BottleSessions** is simple for the programmer to use in both *middleware* and route *views*. The ***Session*** is a superclass of a Python `dict`, accessible as an attribute added to the bottle **`request`** object as **`request.session`**. No special sauce is required to acquire or use the session.
##### Using the session
As an extension to `dict` the *session* is *pythonic* and is used like any other `dict`:
```python
    user = request.session.get('user','Anonymous)
    ...
    request.session.update({
            'groups':['sysadmin','employee'], 
            'ip': request.ip
        })
    request.session['timestamp'] = time.now()
```
More details on using the `BottleSessions.Session` class are [available.](docs/SESSIONS.md)
#### Installation

Install from pypi:
```bash
pip install BottleSessions
```
#### BottleSessions Example 

```python
#app.py:

from BottleSessions import BottleSessions
from bottle import Bottle, request

app = Bottle()
btl = BottleSessions(app)

@app.route('/set/<key>/<val>')
def set_sess(key,val=None):

    request.session[key] = val
    return {key: val}

@app.route('/get/<key>')
def get_sess(key=None):

    return {key: request.session.get(key,'does not exist')}

@app.route('/')
def hello():
    return 'hello world'

if __name__ == '__main__':
    app.run()
#app.py:

from BottleSessions import BottleSessions
from bottle import Bottle, request

app = Bottle()
btl = BottleSessions(app)

@app.route('/set/<key>/<val>')
def set_sess(key,val=None):

    request.session[key] = val
    return {key: val}

@app.route('/get/<key>')
def get_sess(key=None):

    return {key: request.session.get(key,'does not exist')}

@app.route('/')
def hello():
    return 'hello world'

if __name__ == '__main__':
    app.run()

```
Another sample app is [available here](examples/sample_session_app.py)

#### BottleSession Defaults and Tuning

**BottleSessions** default behavior provides a session/cookie life of 300 seconds after last update using a cookie named **bottlecookie** marked `Secure` and `http-only` with `path=/`. The sessions use the same lifetime and are stored in a memory based *cachelib* **SimpleCache**.

These defaults are useful for a range of micro-framework web apps Bottle is typically used for. However, different applications have differing session needs. Hence both cookies and sessions can be [easily customized](docs/OPTIONS.md) to suite a variety of uses.  

#### Backing Store
The backing store is provided by [Pallets Project *cachelib* library](https://pypi.org/project/cachelib/) and uses **SimpleCache** as the default.  

*cachelib* **FileSystemCache**, **RedisCache**, and **Memcached** classes are also supported and can be configured with class specific options:

```python
# config.py - FileSystemCache configuration
cache_config = {
    'cache_type': 'FileSystem',
    'cache_dir' : './sess_dir',
    'threshold': 2000,
    # Additional configuration parameters
    # per cachelib docs
    }
```
```python
# app.py initialization
    ...
from config import cache_config
btl = BottleSessions(app, session_backing=cache_config,
session_cookie='appcookie')
```
Further information is [available on configuring session backing store](docs/BACKING.md) for differing needs and differing cache types.
