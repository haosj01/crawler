#!/usr/bin/python
# -*- coding: UTF-8 -*-

import redis
from setting.project_config import *
import functools
import json
import hashlib

pool = redis.ConnectionPool(host=r_host, port=r_port, decode_responses=True, password=r_password)
r = redis.Redis(connection_pool=pool)


class Cache(object):
    def __init__(self):
        self.r = r
        self.m = m = hashlib.md5()

    def cached(self, timeout=0, key_prefix=None):
        def decorator(func):
            @functools.wraps(func)
            def decorated_function(*args, **kwargs):
                if args:
                    key_path = "_".join(map(str, args))
                elif kwargs:
                    kw = json.dumps(kwargs)
                    key_path = hashlib.md5(kw.encode(encoding='UTF-8')).hexdigest()
                else:
                    key_path = decorated_function.__name__
                key = key_prefix + ":" + key_path
                redis_res = r.get(key)
                if redis_res:
                    res = json.loads(redis_res) if isinstance(redis_res, str) else redis_res
                    return res
                else:
                    res = func(*args, **kwargs)
                    r.set(key, json.dumps(res), ex=timeout, nx=True)
                    return res

            return decorated_function

        return decorator


