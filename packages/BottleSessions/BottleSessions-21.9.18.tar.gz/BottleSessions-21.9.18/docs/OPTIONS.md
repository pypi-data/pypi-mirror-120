#### BottleSession Options
Though designed to be easy to use out of the box, you can still tailor **BottleSessions** for your application needs.  Specific [backing store configuration](docs/BACKING.md) can be tuned along with session behavior to suite a wide range of application needs:
 ```python
    btl = BottleSession(
            app=None, 
            session_backing=None, 
            session_cookie='bottlecookie', 
            session_expire=300,
            session_secure=True,
            session_path='/',
            session_reference='session'
            )
```
**app=_None_** is the app context created by `bottle.Bottle()`. If **app** is passed, **BottleSession** will install it's middleware automatically. Otherwise you can install it later using *`app.install(btl)`*.  Default is *`None`*.

**session_backing=_None_**:  specifies the backing store configuration.  The default is `None`, which creates a __*SimpleCache*__ backing store. This is covered in more detail [elsewhere](docs/BACKING.md)

Either a backing store object (class `BottleSessions.Backing`) or `dict` with **cache_type** and `cachelib` options can be passed as values to **session_backing**.

**session_cookie=_'bottlecookie'_**: this string is the name of the cookie to be used to maintain the session with the web browser.  The default cookie name is **bottlecookie**. 

If you don't like the name, or want to install multiple instances of BottleSessions, you can set the cookie name.

**session_expire=300**: This int is the *__TTL__* (time to live) for both the cookie and cache.  The value is in seconds, and the default is `300` seconds. 

The 'correct' value is application dependent. This is something you probably want to tailor to your use case.

**session_secure=True**: This boolean specifies cookies are marked `secure` - the browser will only pass them over a secure connection (*https*). 
It's never a good idea to pass cookies over *http* as they can be hijacked, but it comes in handy sometimes in dev.

**session_path='/'**: provides the URL path for which the browser provides the cookie to a server. The default is `/` - so any path. Browsers are changing rapidly, and by specifying the path we avoid issues between browser clients making changes. (so eventually I'll have to add `samesite` for that very reason.)

**session_reference='session'**: This string provides the attribute name added to the bottle _`request`_ object for the session.  By default, this is **`session`** as in **`request.session`**.  

If you change this to something else - say `appdata`, then you will access the session as **`request.appdata`**. 

This parameter is also something (along with **session_cookie**) that you need to change if you install multiple instances of BottleSession.

The parameters most useful to configure to use **BottleSessions** on a range of applications are **session_expire** and **session_backing**.

