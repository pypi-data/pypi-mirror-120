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

import logging
import os
import subprocess
from tempfile import gettempdir
from typing import Optional, List, Any, Dict, Sequence

import cli_rack.loader
import cli_rack.utils
from cli_rack_validation import crv

from strome import const
from strome.cache import Cache, FileSystemCacheSerializer
from strome.error import ConfigValidationError


class StromeRuntime:
    def __init__(
        self, config_path: str, config: Optional[dict] = None, root_element_name: str = const.CONF_ROOT_ELEMENT_NAME
    ) -> None:
        self.config_path = config_path
        self.config = config or {}
        self.is_configured = False
        self.__root_element_name = root_element_name
        self.context: Dict[str, Any] = {
            const.RUNTIME_INPUT_FILES: [],
            const.RUNTIME_RESOURCE_PATH: [],
            const.RUNTIME_OUTPUT: {},
        }
        self.__generated_dir = gettempdir()
        self.__libs_meta: List[cli_rack.loader.LoadedDataMeta] = []
        self.is_configured = False

    def init(self):
        if self.flow_config.get(const.CONF_TEMP_DIR) is None:
            self.__generated_dir = os.path.join(self.__generated_dir, "generated")
        else:
            self.__generated_dir = self.flow_config.get(const.CONF_TEMP_DIR)
        os.makedirs(self.__generated_dir, exist_ok=True)
        self.register_resource_path(self.temp_dir)

    @property
    def flow_config(self) -> dict:
        return self.config.get(self.__root_element_name, {})

    @property
    def temp_dir(self) -> str:
        return self.__generated_dir

    @property
    def libs_meta(self) -> List[cli_rack.loader.LoadedDataMeta]:
        return self.__libs_meta

    @property
    def root_config_element(self) -> str:
        return self.__root_element_name

    def register_input_file(self, file_path: str):
        self.context[const.RUNTIME_INPUT_FILES].append(file_path)

    def register_resource_path(self, dir_path: str):
        self.context[const.RUNTIME_RESOURCE_PATH].append(dir_path)

    def register_output(self, pipeline_el: "PipelineElement", key: str, value):
        if key not in pipeline_el.PROVIDES:
            raise ValueError("Attempt to register output data which is not listed in {}.PROVIDES")
        self.context[const.RUNTIME_OUTPUT][key] = value

    def register_lib_meta(self, meta: cli_rack.loader.LoadedDataMeta):
        self.__libs_meta.append(meta)

    def get_output(self, key: str, default_val=None) -> Any:
        return self.context[const.RUNTIME_OUTPUT].get(key, default_val)

    def has_output(self, key: str) -> Any:
        return key in self.context[const.RUNTIME_OUTPUT]


class PipelineElement(object):
    NAME: str
    PARAMS_SCHEMA: dict = {}
    PROVIDES: List[str] = []
    REQUIRES: List[str] = []
    DEPENDENCIES: List[str] = []

    @classmethod
    def name(cls):
        return cls.NAME if cls.NAME is not None else cls.__name__

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.name())
        self.logical_path: Sequence[str] = []

    def _validate_and_normalize_params(
        self, params, raise_error=True, schema: Optional[dict] = None
    ) -> crv.ValidationResult:
        _schema = schema or self.PARAMS_SCHEMA
        with crv.prepend_path(self.logical_path):
            result = crv.validate_and_normalize(params, _schema, False)
        if result.has_errors and raise_error:
            raise ConfigValidationError(
                "Invalid configuration: " + result.error.error_message, self, result  # type: ignore
            )
        return result

    @staticmethod
    def _ensure_dir(dir_name: str):
        cli_rack.utils.ensure_dir(dir_name)

    def load(self):
        pass

    def setup(self, flow_runtime: StromeRuntime, params: dict):
        pass

    def run(self, flow_runtime: StromeRuntime):
        pass


class ExternalExecutableMixin(object):
    @staticmethod
    def run_executable(*args, hide_output=False, mute_output=False) -> subprocess.CompletedProcess:
        return cli_rack.utils.run_executable(*args, hide_output=hide_output, mute_output=mute_output)

    def is_successful_exit_code(self, *args, expected_code=0) -> bool:
        return self.run_executable(*args, mute_output=True).returncode == expected_code


class CacheMixin(object):
    def __init__(self) -> None:
        self.cache: Cache = Cache()

    def setup_cache(self, pipeline_el: PipelineElement, flow_runtime: StromeRuntime):
        cache_file_location = os.path.join(flow_runtime.temp_dir, "_CACHE", pipeline_el.name() + ".json")
        cli_rack.utils.ensure_dir(os.path.dirname(cache_file_location))
        self.cache = Cache(pipeline_el.name(), serializer=FileSystemCacheSerializer(cache_file_location))
        self.cache.load()
