
### About The Session
#### Session notes:
* Sessions are used for authentication and other middleware, shopping carts, forms requiring multiple views, and other web app needs.

* BottleSession sessions are stored on the server-side.  
* Cookies are used for reference only.  The session data can be used by other middleware and views.

* The Session class inherits from the Python `dict` built-in object (_e.g._ `{'a':22}`). The session can be used to store anything a dict can and have it persist between browser requests to the same or different views from the same user.  

* The cookie provides the session identifier used as the key to restore session state, but does not contain the session itself. The cookie only provides the key to retrieve the data from backing store.
* By default the cookies are passed `http-only` and `secure`, and are randomly generated using a cryptically secure algorithm (Python `secrets` documentation.)

* Session state itself is kept in the selected backing store cache.

* There are different backing store cache options that allow customization to specific application needs. See the [details on backint store.](BACKING.md)

* BottleSession __*lazy loads*__ sessions. The data itself is only rehydrated (retrieved from backing store) when the session object is references.

* Sessions are writen back only if they have are _dirty_ - that is, they have been modified, or when they have been directly saved. 

#### Session Methods

First off - the session is a `dict`, so any of the methods (get, copy, pop, update, etc.) as well as the syntactic sugar of Python dictionaries - (_e.g._ session['a'] = 22` is sugar for `session.__setitem__('a',22)`) - are all supported.

You can clear a session like a dict, by calling _`session.clear()`_, and for general use that is a fine way to empty the data. This is now a modified session that will be flushed to backing store by the middleware at the end of the request. This is true for any of the `dict` methods that change data (_setitem(), update(), pop(), etc._) 

The **`Session`** class adds only a couple for public use:
```python
    session.session_delete()

    session.session_save(expire=t, force=False)

    session.session_modified = True
```
##### session.session_delete()
BottleSessions provides `session.session_delete()`. This clears the session (like `session.clear()`), but also assures it is _removed_ from backing store immediately. This is useful in error conditions or even something like a logoff.  A delete session can't be used and will not be flushed to backing store.
##### session.session_modified
While updating session directly - say `session['username'] = 'alice'` the change to the session is detected, marking it *dirty*, and hence to flush it to backing store. Cool.

Other updates to an extended session dict may not be detected.  Consider:
```python
    session['userdata']['language'] = 'Python'
```
As the session object itself is never updated: the modification isn't detected by the object itself. We have to mark the session _dirty_ ourselves:

```python
    session.session_modified = True
```
The middleware will take care of flushing changes to backing store for us.
##### session.session_save(expire,force)
As an alternative to having the middleware flush to backing store, we can call `session.session_save()` directly in our view or other middleware:
```python
    session.session_save(expire=3600, force=True)
```
This will serialize the session data and save modified data in backing store right now. The _**force**_ assures it is written back, even if it unmodified (but deleted sessions will not be flushed).

This will also extend the TTL of the cookie and backing store, and allow other middleware to adjust the TTL for their needs. This is something we may have need for in some apps.

##### session.session_regenerate()
The sessions `session_id` is typically maintained by the client in a cookie. It is a good idea to rotate the `session_id` after login or other security events. `session.session_regenerate()` does this, generating a new random session identifier, associating this with the session, rendering the old session id useless.