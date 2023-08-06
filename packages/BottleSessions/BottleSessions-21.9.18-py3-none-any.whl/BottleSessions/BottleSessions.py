import os
import sys
from secrets import token_urlsafe

from .backing import Backing
from .Session import Session

from bottle import request, response, PluginError

DEBUG = os.environ.get('DEBUG_SESSIONS', False)

default_backing_options = {
    'cache_type': 'SimpleCache',
}

def dprint(*args):
    """Debug Print"""
    if DEBUG:
        print(*args, file=sys.stderr)


class BottleSessions:
    """
    Create a BottleSession

    BottleSession(
            app, 
            session_backing, 
            session_cookie, 
            session_expire,
            session_secure,
            session_path,
            session_reference
            )

    Install middleware to provide sessions that persist accross http requests for a given
    client using http cookies and a backing object.

    Arguments:

    app:                the Bottle object - if provided instance self-installs 
                        default: None - instance does not self-install

    session_backing:    persistent backing for session objects
                        default: SimpleCache - creates a memory based cache
    
    session_cookie:     the name of the cookie used to track the session
                        default: 'bottlecookie'
                        environment: SESSION_COOKIE overrides parameter
    
    session_expire:     cookie life (and cache) life of the session object
                        default: 300 Sec (from last session update)
                        environment: SESSION_LIFE overrides parameter
    
    session_secure:     set the cookie with the 'Secure' flag
                        default: True (also true in bottle debug mode)
                        environment: SESSION_SECURE overrides parameter
    
    session_path:       http URL path the browser will provide the cookie
                        default '/' - any path on the site
                        environment: SESSION_PATH overrides parameter

    session_reference:  the name used to attach the session to the request object
                        default is 'session' (e.g. request.session )
                        environment: none

    If multiple BottleSessions are used in the same app, both session_reference and 
    session_cookie must be unique (this precludes using multiple sessions with environment 
    variables.)

    """
    name = 'BottleSession'      # Bottle Plugin API v2 required (this is updated)
    api = 2                     # Bottle Plugin API v2 required
    
    def __init__(self,
            app = None,                         # if app exists, module self-installs
            session_backing=None,               # Backing object, dict of config, or None
            session_cookie='bottlecookie',      # name of session cookie
            session_expire= 300,                # default ttl for cache and cookie
            session_secure= True,               # Secure Cookie
            session_path='/',                   # Cookie path
            session_reference='session'         # name of request reference to add for session
        ):
        """
        BottleSession.__init__()

        - establishes backing store
        - manage cookie specifications
        - installs self if app was provided
        """
        # This is the name of this plugin, and the name set for the
        # session when added to the request.
        self.name = session_reference

        if session_backing is None:
            self.backing = Backing(**default_backing_options)

        elif type(session_backing) is dict:
            self.backing = Backing(**session_backing)

        else:
            self.backing = session_backing
        
        self.cookie_name = os.environ.get('SESSION_COOKIE', session_cookie)
        self.cookie_expire = int(os.environ.get('SESSION_LIFE', session_expire))
        self.cookie_secure = os.environ.get('SECURE_COOKIE', session_secure)
        self.session_path = os.environ.get('SECURE_PATH', session_path)

        # self-install session middleware
        if app:
            app.install(self)

        print(f'*** Session "{self.name}" initialized using "{self.backing.cache_type}"')
        

    def setup(self, app):
        """
        setup()

        - Bottle plugin v2 api required
        - runs on plugin install
        - validate unique cookie names for multiple instances
        - validate unique session_reference names for multiple instances
        """

        for plugin in app.plugins:
        
            if isinstance(plugin, BottleSessions):
                # Multiple instantiations are permited with unique names and cookies.
                if plugin.name == self.name:
                    # name must be unique
                    emsg = f'\n\nError: BottleSession Duplicate name (session_reference) "{self.name}"\n'
                    raise PluginError(emsg)

                if plugin.cookie_name == self.cookie_name:
                    # cookies must be unique
                    emsg = f'\n\nError: BottleSession Duplicate cookie "{self.cookie_name}" allocated for "{plugin.name}" and "{self.name}"\n'
                    raise PluginError(emsg)
    

    def close(self):
        """
        close()

        Bottle plugin v2 api required
        - runs on plugin uninstall
        - nothing to do
        """
        pass


    def apply(self, f, context):
        """
        apply()

        - Bottle plugin v2 api required 
        - runs to decorate each applied path
        - adds wrappers to views
        - wrapper adds session_reference to request object
        """

        def session_wrapper(*args, **kwargs):
            """
            Middleware code in request path
            - retrieves session object for cookie from backing store
            - sets session_reference on request object
            - saves changed sessions to backing store
            - updates client cookie in each response (except in exceptions)
            """

            # find or create a session based on the requests cookies
            key = request.get_cookie(self.cookie_name)
            session = Session(backing=self.backing, session_id=key)
            dprint('initiated session')
            # attach to request for use by views or successive middleware            
            setattr(request, self.name, session)
            dprint('attached')
            # next middleware or run the view
            body =  f(*args, **kwargs)
            
            # save the session
            session.session_save(expire=self.cookie_expire)

            # Add the Set-Cookie header        
            self.set_session_cookie(session)
            
            return body

        return session_wrapper


    def set_session_cookie(self, session):
        """
        set_session_cookie()

        - runs on response path of route decoration
        - set cookie if it was updated to backing store
        - expire deleted cookies

        """

        if session.session_is_saved or session.session_deleted:
            # why bother reset the cookie life if we don't write clean 
            # sessions to the backing store?

            t = -1 if session.session_deleted else self.cookie_expire
            
            response.set_cookie(
                name=self.cookie_name,
                value=session.session_id,
                max_age = t,
                httponly = True,
                path = self.session_path,
                secure = self.cookie_secure
            )

