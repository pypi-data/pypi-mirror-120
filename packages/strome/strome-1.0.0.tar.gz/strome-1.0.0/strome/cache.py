#    Strome - Micro-framework for Python for building processing pipelines
#    Copyright (C) 2021 Dmitry Berezovsky
#    The MIT License (MIT)
#
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import datetime
import json
import logging
import os
from abc import ABC
from typing import Dict, Optional, Any, Type

import cli_rack.serialize

LOGGER = logging.getLogger("cache")


class CacheSerializer(ABC):
    META_UPDATED_AT = "updated_at"
    META_PERSISTED_AT = "persisted_at"
    META_LOADED_AT = "loaded_at"
    META_NAME = "cache_name"
    CACHE_DATA = "data"

    def persist(self, cache: "Cache", data: dict):
        raise NotImplementedError

    def load(self) -> Dict:
        raise NotImplementedError


class InMemoryCacheSerializer(CacheSerializer):
    def persist(self, cache: "Cache", data: dict):
        pass

    def load(self) -> Dict:
        return {}


class FileSystemCacheSerializer(CacheSerializer):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path

    def persist(self, cache: "Cache", data: dict):
        with open(self.file_path, "w") as f:
            cache_dict = {
                CacheSerializer.META_UPDATED_AT: cache.last_updated_at,
                CacheSerializer.META_PERSISTED_AT: cache.persisted_at,
                CacheSerializer.META_NAME: cache.name,
                CacheSerializer.CACHE_DATA: data,
            }
            json.dump(cache_dict, f, cls=cli_rack.serialize.DateTimeEncoder)

    def load(self) -> Dict:
        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    return json.load(f, cls=cli_rack.serialize.DateTimeDecoder)
                except json.decoder.JSONDecodeError as e:
                    LOGGER.warning(
                        "Unable to read cache file {} (REASON: {}). Cache might be corrupted. "
                        "Starting with empty cache. ".format(self.file_path, str(e))
                    )

        return {}


class Cache(object):
    def __init__(self, name="default", serializer=InMemoryCacheSerializer()) -> None:
        self.__last_updated: Optional[datetime.datetime] = None
        self.__persisted_at: Optional[datetime.datetime] = None
        self.__loaded_at: Optional[datetime.datetime] = None
        self.__cache: Dict[str, Any] = {}
        self.__serializer = serializer
        self.name: str = name

    def get(self, key: str, default_val: Any = None) -> Any:
        return self.__cache.get(key, default_val)

    def put(self, key: str, val: Any) -> None:
        self.__cache[key] = val
        self.__last_updated = datetime.datetime.now()

    def has(self, key: str):
        return key in self.__cache

    def get_or_raise(self, key: str, exc: Type[Exception] = KeyError):
        if self.has(key):
            return self.get(key)
        else:
            raise exc('Cache {} doesn\'t have key "{}"'.format(self.name, key))

    def load(self) -> None:
        data_dict = self.__serializer.load()
        self.__loaded_at = datetime.datetime.now()
        self.__persisted_at = data_dict.get(CacheSerializer.META_PERSISTED_AT)
        self.__last_updated = data_dict.get(CacheSerializer.META_UPDATED_AT)
        self.__cache = data_dict.get(CacheSerializer.CACHE_DATA, {})

    def persist(self) -> None:
        self.__serializer.persist(self, self.__cache)

    @property
    def has_changes(self):
        return self.__last_updated is not None

    @property
    def persisted_at(self) -> Optional[datetime.datetime]:
        self.__persisted_at = datetime.datetime.now()
        return self.__persisted_at

    @property
    def last_updated_at(self) -> Optional[datetime.datetime]:
        return self.__last_updated

    @property
    def loaded_at(self) -> Optional[datetime.datetime]:
        return self.__loaded_at
