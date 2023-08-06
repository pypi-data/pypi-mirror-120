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
import sys
from typing import NamedTuple, List, Union, Type

import cli_rack.loader
import cli_rack.utils
from cli_rack.utils import safe_cast
from strome import processors
from strome import const
from strome.error import InvalidModuleError, ConfigValidationError
from strome.pipeline import PipelineElement, StromeRuntime
from strome.utils import deepmerge_dict

LOGGER = logging.getLogger("strome.core")

DEFAULT_PROCESSORS_CONFIG = {
    const.CONF_PIPELINE: ["jinja2"],
    const.CONF_TEMP_DIR: "generated",
    const.CONF_LIB_DIR: "build-libs",
    const.CONF_CLASSPATH: [],
    const.CONF_LIBS: [],
}


class PipelineItem(NamedTuple):
    pipeline_element: PipelineElement
    pipeline_params: dict


Pipeline = List[PipelineItem]


def setup_pipeline(pipeline_def: List[Union[dict, str]], flow_runtime: StromeRuntime) -> Pipeline:
    pipeline: List[PipelineItem] = []
    for cfg in pipeline_def:
        processor_name = cfg if isinstance(cfg, str) else safe_cast(str, cfg.get(const.CONF_PIPELINE_NAME))
        params = {} if isinstance(cfg, str) else cfg.get(const.CONF_PIPELINE_PARAMS, {})
        try:
            if not processors.REGISTRY.exists(processor_name):
                if not __is_fully_qualified_name(processor_name):
                    raise InvalidModuleError("Processor {} is unknown".format(processor_name))
                else:
                    load_module(processor_name)
            pipeline_element = processors.REGISTRY.get_by_name(processor_name)()  # type: ignore
        except KeyError:
            raise ValueError("Invalid pipeline configuration. Processor {} is unknown".format(processor_name))
        pipeline_element.load()
        pipeline.append(PipelineItem(pipeline_element, params))
    for p in pipeline:
        if isinstance(p.pipeline_element.REQUIRES, list):
            for x in p.pipeline_element.REQUIRES:
                if not flow_runtime.has_output(x):
                    raise ValueError(
                        "{} expects {} to be provided by other processor, "
                        "but it is not registered in the context. "
                        "Check if your pipeline is configured correctly".format(p.pipeline_element.name(), x)
                    )
        p.pipeline_element.setup(flow_runtime, p.pipeline_params)
        if isinstance(p.pipeline_element.PROVIDES, list):
            for x in p.pipeline_element.PROVIDES:
                flow_runtime.register_output(p.pipeline_element, x, None)
    return pipeline


def run_pipeline(pipeline: Pipeline, flow_runtime: StromeRuntime):
    for p in pipeline:
        p.pipeline_element.run(flow_runtime)


def __lib_path_resolver(meta: cli_rack.loader.LoadedDataMeta):
    if os.path.isdir(os.path.join(meta.path, "src")):
        return "src"
    return ""


def __is_fully_qualified_name(name: str):
    return "." in name


def load_libs(flow_runtime: StromeRuntime, force_reload=False):
    locators = safe_cast(List, flow_runtime.flow_config.get(const.CONF_LIBS))
    if len(locators) > 0:
        cli_rack.utils.ensure_dir(cli_rack.loader.DefaultLoaderRegistry.target_dir)
    for locator in locators:
        if not isinstance(locator, cli_rack.loader.BaseLocatorDef):
            pass
        meta = cli_rack.loader.DefaultLoaderRegistry.load(locator, __lib_path_resolver, force_reload)
        flow_runtime.register_lib_meta(meta)


def load_context_path(flow_runtime: StromeRuntime):
    context_path = flow_runtime.flow_config.get(const.CONF_CLASSPATH, [])
    for p in context_path:
        sys.path.append(p)
    for meta in flow_runtime.libs_meta:
        sys.path.append(os.path.join(meta.path, meta.target_path))


def preload_modules(flow_runtime: StromeRuntime):
    modules_to_load = safe_cast(List, flow_runtime.flow_config.get(const.CONF_PRELOAD, []))
    for m in modules_to_load:
        load_module(m)


def import_class(class_name_or_class: Union[str, Type]):
    if isinstance(class_name_or_class, str):
        try:
            module_name, class_name = class_name_or_class.rsplit(".", 1)
            module = __import__(module_name, globals(), locals(), [class_name], 0)
            clazz = getattr(module, class_name)
        except ImportError as e:
            raise InvalidModuleError("Class doesn't exist: " + str(class_name_or_class), e)
        except AttributeError as e:
            raise InvalidModuleError("Class doesn't exist: " + str(class_name_or_class), e)
    else:
        clazz = class_name_or_class
    # Validations
    assert clazz is not None, "module instance shouldn't be None"
    return clazz


def __import_processor(class_name_or_class: str) -> Type[PipelineElement]:
    clazz = import_class(class_name_or_class)
    if not issubclass(clazz, PipelineElement):
        raise InvalidModuleError("Processor must implement strome.preprocessor.PipelineElement")
    return clazz


def load_module(class_name: str):
    LOGGER.info("Loading module " + class_name)
    processor_cls = __import_processor(class_name)
    processors.REGISTRY.register(processor_cls, aliases=(class_name,))
    LOGGER.info("\t\tModule {}({}) loaded".format(class_name, processor_cls.name()))


def process_strome_config(  # noqa: C901
    config_dict: dict, flow_runtime: StromeRuntime, default_strome_conf: dict = None
):
    if flow_runtime.root_config_element in config_dict:
        flow_runtime.is_configured = True
        # Ensure preprocessor context is declared
        conf_strome = config_dict[flow_runtime.root_config_element]
        if not isinstance(conf_strome, dict):
            raise ValueError("{} must be dictionary".format(flow_runtime.root_config_element))
        if default_strome_conf is None:
            default_strome_conf = DEFAULT_PROCESSORS_CONFIG
        config_dict[flow_runtime.root_config_element] = deepmerge_dict(
            default_strome_conf, conf_strome, merge_lists=False
        )
        # Validate classpath
        classpath = flow_runtime.flow_config.get(const.CONF_CLASSPATH)
        if classpath:
            for path in classpath:
                if isinstance(path, str):
                    if not os.path.exists(path):
                        raise ConfigValidationError(
                            "Path " + path + " doesn't exist",
                            config_section=flow_runtime.root_config_element + "/" + const.CONF_CLASSPATH,
                        )
                else:
                    raise ConfigValidationError(
                        "Context path must be the list of strings",
                        config_section=flow_runtime.root_config_element + "/" + const.CONF_CLASSPATH,
                    )
        # Validate libs
        cli_rack.loader.DefaultLoaderRegistry.target_dir = flow_runtime.flow_config.get(const.CONF_LIB_DIR)
        lib_locators: List[cli_rack.loader.BaseLocatorDef] = []
        libs = flow_runtime.flow_config.get(const.CONF_LIBS)
        if libs is not None:
            for i, lib_def in enumerate(libs):
                try:
                    lib_locators.append(cli_rack.loader.DefaultLoaderRegistry.parse_locator(lib_def))
                except cli_rack.loader.LoaderError as e:
                    raise ConfigValidationError(
                        "Invalid library definition: " + str(e),
                        config_section=flow_runtime.root_config_element + "/" + const.CONF_LIBS,
                    )
            if len(lib_locators) > 0:
                flow_runtime.flow_config[const.CONF_LIBS] = lib_locators
