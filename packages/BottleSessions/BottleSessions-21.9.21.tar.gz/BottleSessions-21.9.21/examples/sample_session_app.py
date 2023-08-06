import os
import sys
from bottle import request, Bottle
from BottleSessions import BottleSessions

DEBUG=os.environ.get('DEBUG',False)

dprint = lambda *args, **kwargs: print(*args, **kwargs, file=sys.stderr)
app = Bottle()

CACHE_TYPE = os.environ.get('CACHE_TYPE', 'SimpleCache')

if CACHE_TYPE == 'SimpleCache':
    #
    # By default, cachelib SimpleCache is used for session backing.
    #  - this is non-persistent.
    #  - options are all defaults (default_timeout=300 threshold=500)
    #    but you can set these as either kwargs or session_backing
    #
    btl = BottleSessions(app)

elif CACHE_TYPE == 'FileSystem':
    #
    # The session backing can be explicitly established
    # This permits it to be put to other use by your application.
    #
    # the 'cache_type=' argument selects the cachelib type. All other arguments are passed to 
    # cachelib. Each cachelib type has some required and some optional configuration arguments.
    # 
    # Pass this object when creating the BottleSessions object using the 'session_backing='
    # argument.
    #
    from BottleSessions import Backing

    file_backing = Backing(cache_type='FileSystem', cache_dir='./.cache_dir')
    btl = BottleSessions(app, session_backing=file_backing)

elif CACHE_TYPE == 'Redis':
    #
    # You can pass all of the Backing options to BottleSession as a dict using the 'session_backing'
    # option, and BottleSessions will create the Backing object instance.
    #
    btl = BottleSessions(app, session_backing={
                'cache_type': 'Redis',
                'host': 'localhost',    # This is the default for cachelib redis
                'port' : '6379',        # This is the default for cachelib redis
            })

elif CACHE_TYPE == 'Memcached':
    #
    # If you want to explictly install BottleSessions
    # don't pass 'app', and install it with app.install()
    # - useful if you want your middleware installed in
    #   a particluar order
    #
    memcache_options = {
        'servers': ['localhost:11211'],
        'key_prefix': 'MyAppPrefix',
        'cache_type': 'Memcached'
    }

    btl = BottleSessions(session_backing=memcache_options)
    # do other things here...
    app.install(btl)

else:
    emsg = f'CACHE_TYPE "{CACHE_TYPE}" is unsupported'
    raise Exception(emsg)
#
# Multiple instantiations of BottleSession can be made, however the session_reference
# and session_cookie must be different
#

@app.route('/')
def index():
    """Report the current counter"""

    return f"The counter is at {request.session.get('cnt',0)}"


@app.route('/p')
def add_one():
    """Add one to the current session counter"""
    
    sess = request.session
    cnt = sess.get('cnt',0) +1
    sess['cnt'] = cnt

    return f'counter is up to {cnt}'    


@app.route('/n')
def sub_one():
    """Subtract one from the current session counter"""

    sess = request.session
    cnt = sess.get('cnt', 0) - 1
    sess['cnt'] = cnt

    return f'counter is down to {cnt}'


if __name__ == '__main__':
    app.run(host='localhost', port=8001, debug=DEBUG)