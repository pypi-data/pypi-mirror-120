rlog-async
====
Fork of https://github.com/lobziik/rlog

Difference: communications with redis in another thread, so log in unavailable redis doesn't affect your app.   

Installation
------------
From pypi:

    $ pip install rlog-async
From source:

    $ sudo python setup.py install

Usage
-----

    >>> from rlog import RedisHandler
    >>> logger = logging.getLogger()
    >>> logger.addHandler(RedisHandler(channel='test'))
    >>> logger.warning("Spam!")
    >>> logger.error("Eggs!")

Redis clients subscribed to ``test`` will get a json log record by default.

_RedisHandler_ and _RedisListHandler_ also accepted all redis client settings as kwargs. More info about client settings
you may find in [redis-py](https://github.com/andymccurdy/redis-py) documentation.

Custom formatters also supported, handlers accept this as _formatter_ keyword argument. JSONFormatter from this package
used as default. 

You can use the ``redis-cli`` shell that comes with ``redis`` to test this.  At
the shell prompt, type ``subscribe my:channel`` (replacing with the channel
name you choose, of course). You will see subsequent log data printed in the
shell.


Also you can use it with Django:
```Python
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'handlers': {
            'redis': {
                'level': 'DEBUG',
                'class': 'rlog_async.RedisHandler',
                'host': 'localhost',
                'password': 'redis_password',
                'port': 6379,
                'channel': 'my_amazing_logs'
            }
        },
        'loggers': {
            'django': {
                'level': 'INFO',
                'handlers': ['redis'],
                'propagate': True,
            },
        }
    }
```

You can also simply use it with logstash.
