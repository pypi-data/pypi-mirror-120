"""
Backing

Backing offers abstraction of Pallets' cachelib, the underlying cache used, and
is to minimize changes required to utilize and change the cache selection without
needing to update code, just configuration data.

'SimpleCache'   ->  cachelib.SimpleCache.
                Default, non-persistant caching.

'FileSystem'    ->  cachelib.FileSystemCache.
                Persistant caching to a filesystem.

                The argument 'cache_dir' is required, others are optional.

'Redis'         ->  cachelib.RedisCache
                Persistant, potentially network based and shared.

                By default this uses a local instance of redis.

'Memcached'     ->  cachelib.MemcachedCache
                Persistant, potentially network based and shared.

                Requires 'servers' argument, e.g. servers=['localhost:11211']

Generally cachelib default expiration is 300 seconds.

Methods:

Underlying methods of cachelib.BaseCache:

    All cachelibs support at least delete(), get(), has(), and set().
    For most uses, these are what you need.
    
    Some cachelibs also support add(), clear(), dec(), inc(),
    delete_many(), get_many(), and set_many()

Refer to https://cachelib.readthedocs.io/ for details to see which methods are
implemented by each system and detailed explainations.  

"""
import sys
from cachelib import SimpleCache, RedisCache, MemcachedCache, FileSystemCache


_caches = {
    'FileSystem': FileSystemCache, 
    'Memcached': MemcachedCache,
    'Redis': RedisCache, 
    'SimpleCache': SimpleCache
    }

class Backing:
    
    def __init__(self, cache_type='SimpleCache', **kwargs):
        """
        back = Backing(cache_type, **kwargs)

        cache_type 
        - this can be 'FileSystem', 'Memcached', 'Redis', or (default) 'SimpleCache'
        - selects the associated Pallets cachelib and instantiates it
        
        kwargs
        - keyword arguments appropriate for the selected cache_type and are passed to cache_lib
        - Each type may have a different set of required and optional arguments based on the
          underlying technology.  See the cachelib documentation.

        """

        if cache_type not in _caches:
            raise Exception(f'Backing: cache_type "{cache_type}" unsupported')

        CacheBase = _caches[cache_type]
        self.cache = CacheBase(**kwargs)

        self.cache_type = cache_type

        print(f'INFO: {__name__} cache "{cache_type}" established', file=sys.stderr)

    
    def __getattr__(self, name):
        """Retrieve attr from underlying cache """

        return getattr(self.cache, name)
