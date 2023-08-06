import json
import os
import sys
from secrets import token_urlsafe

from cachelib.simple import SimpleCache

from .backing import Backing


DEBUG = os.environ.get('DEBUG_SESSIONS', False)
TOKENLEN = 16      # Length of session key

def dprint(*args):
    """Debug Print"""
    if DEBUG:
        print(*args, file=sys.stderr)

def ddprint(*args):
    if DEBUG == '2':
        print(*args, file=sys.stderr)


default_backing = None
default_backing_config = {
    'cache_type': 'SimpleCache',
}

def _get_default_backing(backing):
    """
    _get_default_backing(backing)
    
    Returns the prefered backing store 
    - if user provides a valid Backing object, use it
    - if there is a default_backing object instantiated, use it
    - if the user provided a configuration dict, use it to create
      a new default_backing object
    - otherwise, create a default_backing object using our defaults.
    
    """
        # Probably they didn't mean to do this...
    global default_backing, default_backing_config

    if isinstance(backing, Backing):
        return backing

    if default_backing:
        return default_backing
    
    elif type(backing) is dict:
        default_backing = Backing(**backing)    

    else:
        # create a new default backing
        default_backing = Backing(**default_backing_config)
        
    return default_backing


class Session(dict):
    """
    
    session = Session(backing, sess_id)

    Each session is an object (dict) backed with persistent storage such that it 
    can be recalled on subsequent requests with its key.  Sessions are lazy loaded
    from backing.

    Arguments:

    session_backing:    The Backing object storing the desired key
                        default: None - creates a new, default backing store.

    session_id:         The session id is the key of the object to be retrieved.
                        default: None - creates a new key and object

    Sessions are saved to backing store as json if they have been modified, via
    session.save_session().  Only modified sessions are saved.  
    
    Updating a session dict (e.g. session['user'] = 'alice' or session.clear()) sets 
    them as modified. They can also be explicitly set as modified explicitly by setting 
    session.modified = True. 
    
    This may be required for indirect updates.
    e.g.
        session['user_attributes']['email'] = 'alice@example.org'
        session.session_modified = True
    
    """
    
    def __init__(self, backing=None, session_id=None):

        dict.__init__(self)

        self.session_backing = _get_default_backing(backing)
        self.session_id = session_id

        self.session_dict = False           # dict is loaded and valid
        self.session_modified =  False      # dict has been modified
        self.session_deleted =  False       # dict has been deleted

        self.session_is_saved = False       # useful for when to set cooikes

    #
    # session is loaded from backing store and marked valid only if it is accessed.
    # 
    # session is marked dirty if it modifed.
    #
    def __contains__(self, key):
        """
        session.__contains__()
        
        membership: x in session:
        - assure the dict is loaded
        - run the super call
        """
        ddprint(f'Session: contains {key}')

        if not self.session_dict: self.session_lazy_load()

        return super().__contains__(key)
    

    def __iter__(self):
        """
        session.__iter__()

        Iterator: For x in session:
        - assure the dict is loaded
        - run the super call
        """
        ddprint(f'Session: iter')

        if not self.session_dict: self.session_lazy_load()

        return super().__iter__()


    def __getitem__(self, key):
        """
        session.__getitem__()

        Get item from dict:
        - assure the dict is loaded
        - run the super call
        """
        ddprint(f'Session: getitem {key}')

        # lazy load may be required
        if not self.session_dict: self.session_lazy_load()
        
        return super().__getitem__(key)


    def __setitem__(self, key, val):
        """
        session.__setitem__()

        Set item in dict
        - assure the dict is valid
        - mark session as dirty
        - run the super call
        """
        ddprint(f'Session setitem {key} = {val}')
        
        # lazy load may be required
        if not self.session_dict: self.session_lazy_load()

        # Mark session dirty
        self.session_modified = True

        return super().__setitem__(key, val)


    def __getattribute__(self, name):
        """
        Handle dict method calls
        - handle 'session_*' calls with super
        - otherwise assure dict is valid
        - routines that write set modified flag
        - run the super
        """
        ddprint(f'Session: getattr {name}')

        if name.startswith('session_'):
            # escape geattr loops
            return super().__getattribute__(name)
        
        # lazy load may be required
        if not self.session_dict: self.session_lazy_load()

        # if a method is called that updates, set the session modified
        if name in ['clear', 'pop', 'popitem', 'setdefault', 'update']:
            self.session_modified = True

        return super().__getattribute__(name)

    
    def __str__(self):
        """
        session.__str__()

        Displayable string showing the session details
        """

        if self.session_dict:
            sdict = super().__str__() + ' >'
        else:
            sdict = '[ No data cached ]'

        tstat = f'<Session: [{self.session_id}] (' 
        tstat += ' dirty ' if self.session_modified else '' 
        tstat += ' deleted ) ' if self.session_deleted else ')'

        return tstat + sdict

    #
    # Internal methods to manage creating or reconstition of sessions from backing store
    #
    def session_lazy_load(self):
        """
        self.session_lazy_load()
        
        Load the session from backing store
        - verify we are not deleted
        - using either session_load() or session_new()

        """

        if self.session_deleted:
            raise Exception(f'Referencing deleted session {self.session_id}')

        # lazy load the session
        if self.session_id:
            dprint(f'Session: {self.session_id} attempting lazy load')
            self.session_load()

        else:
            dprint(f'Session: creating new key and session')
            self.session_new()    


    def session_load(self):
        """
        session.session_load()

        Load (or reload) session state from backing store
        - retrieves 'key' from backing store
        - deserializes the json into the session dict
        - set dict_valid if everything works
        - tempermental situations cause a session_new created
        """
        
        dprint(f'Session: {self.session_id} loading data')
        serial = self.session_backing.get(self.session_id)
        
        if serial:
            # just in case it fails to deserialize
            try:
                data_dict = json.loads(serial)

                super().clear()
                super().update(data_dict)

                self.session_dict = True
                self.session_modified = False

                dprint(f'Session: {self.session_id} load complete')

                return

            except:
                # data is bad - we'll pretend it's a new session
                dprint(f'Session: {self.session_id} failed to reload data')

        else:
            # Not found in backing store - create a new session
            dprint(f'Session: {self.session_id} no backing store')

        dprint(f'Session: {self.session_id} creating new session for this key')

        self.session_new()


    def session_new(self):
        """
        session.session_new()

        Generate a new session
        - Reuse an existing or cerate a sess_id
        - set session_dict
        - create an empty dict. 
        """

        if self.session_id is None:
            self.session_id = token_urlsafe(TOKENLEN)
        
        super().clear()

        self.session_dict = True

        dprint(f'Session: {self.session_id} new session created')

    #
    # Methods for Session users:  delete(), clear(), and save_session()
    #     
    def session_delete(self):
        """
        session.session_delete()

        Mark this session to be deleted
        - remove from backing store
        - set deleted flag to prevent flushing
        - mark as invalid
        """

        if self.session_dict is None:
            self.session_backing.delete(self.session_id)
        
        self.clear()
        self.session_dict = False
        self.session_deleted = True



    def session_save(self, expire=0, force=False):
        """
        session.session_save()

        Save session to backing store
        - only of not deleted set
        - must be modified or have force set
        - force does not flush a deleted session
        """
        
        if not self.session_deleted and (self.session_modified or force):
            # save this session to backing store
            serial = json.dumps(self)
            
            self.session_backing.set(self.session_id, serial, expire)
            self.session_modified = False
            self.session_is_saved = True

            dprint(f'Session {self.session_id} - flushed to backing store')
        else:
            dprint(f'Session: {self.session_id} - not dirty/notflushed')
    

    def session_regenerate(self):
        """
        session.session_regenerate()

        Generate a new sessionid
        - assure dict is valid
        - set session_id to new id
        - mark session dirty
        - remove old session_id from backing store
        """

        if not self.session_dict : self.session_lazy_load()

        old_session_id = self.session_id
        self.session_id = token_urlsafe(TOKENLEN)
        self.session_modified = True
        self.session_backing.delete(old_session_id)

