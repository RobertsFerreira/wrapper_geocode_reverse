import time

import pytest
from wrapper_geocode_reverse.src.core.cache.simple_cache import SimpleCache


def test_cache():
    cache = SimpleCache()
    cache.set('foo', 'bar')
    item = cache.get('foo')
    if item is None:
        pytest.fail('item not found')
    assert item == 'bar'

def test_get_nonexistent_cache():
    cache = SimpleCache()
    assert cache.get('nonexistent_key') is None

def test_ttl_cache():
    cache = SimpleCache()
    cache.set('foo', 'bar', ttl=5)
    time.sleep(6)
    assert cache.get('foo') is None
    
def test_remove_expired_cache():
    cache = SimpleCache()
    cache.set('foo', 'bar', ttl=5)
    time.sleep(6)
    cache.remove_expired()
    assert cache.get('foo') is None

def test_lru_policy():
    cache = SimpleCache(capacity=2)
    cache.set('foo', 'bar', ttl=15)
    cache.set('bar', 'baz')
    cache.get('foo')
    cache.set('qux', 'que')
    assert len(cache.cache) == 2
    assert cache.get('bar') is None


def test_reuse_cache():
    cache = SimpleCache()
    cache.set('foo', 'bar')
    cache.get('foo')
    item = next(reversed(cache.cache))
    assert item == 'foo'

def test_reset_ttl_cache():
    cache = SimpleCache()
    time_actually = time.time()
    ttl = 5
    cache.set('foo', 'bar', ttl=ttl)
    time_actually = time_actually + ttl
    time.sleep(3)
    ttl = 10
    cache.set('foo', 'bar', ttl=ttl)
    time_actually = time_actually + ttl
    time.sleep(4)
    item = cache.get('foo')
    if item is None:
        pytest.fail('item should not be None')
    assert item == 'bar'