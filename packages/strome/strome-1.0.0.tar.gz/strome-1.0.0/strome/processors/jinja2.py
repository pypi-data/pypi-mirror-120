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
import os
from os import path
from tempfile import gettempdir
from typing import List, Optional, Dict, Any

import jinja2
from jinja2 import FileSystemLoader

from cli_rack_validation import crv
from cli_rack.utils import safe_cast, none_throws
from strome.const import CONF_INPUT_FILES, CONF_CONTEXT, CONF_CONTEXT_FILES, RUNTIME_OUTPUT
from strome.pipeline import PipelineElement, StromeRuntime
from strome.utils import yaml_file_to_dict, deepmerge_dict

__all__ = ("Jinja2Processor",)

PARAM_OUTPUT_DIR = "output-dir"
PARAM_TAG_LIBS = "tag-libs"
PARAM_SEARCH_PATH = "search-path"

RUNTIME_CONTEXT_VARS = "context-vars"
RUNTIME_JINJA2_OUTPUT_FILES = "jinja2-output-files"


class Jinja2Processor(PipelineElement):
    NAME = "jinja2"
    PROVIDES = [
        RUNTIME_JINJA2_OUTPUT_FILES,
    ]
    PARAMS_SCHEMA = {
        PARAM_TAG_LIBS: crv.ensure_list(crv.string),
        PARAM_OUTPUT_DIR: crv.string,
        crv.Required(PARAM_SEARCH_PATH, default=[""]): crv.ensure_list(crv.string),
    }

    def __init__(self) -> None:
        super().__init__()
        self.output_dir = gettempdir()
        self.search_path: List[str] = [""]
        self.jinja_options: Dict[str, Any] = {}
        self.__jinja_env: Optional[jinja2.Environment] = None

    def setup(self, flow_runtime: StromeRuntime, _params: dict):
        # HANDLE PARAMS
        default_output_dir = path.join(flow_runtime.temp_dir, "jinja2")
        params: Dict[str, Any] = none_throws(self._validate_and_normalize_params(_params).normalized_data)
        # PARAM: output dir
        self.output_dir = params.get(PARAM_OUTPUT_DIR, default_output_dir)
        self._ensure_dir(self.output_dir)
        flow_runtime.register_resource_path(self.output_dir)
        # PARAM: Search Path
        self.search_path = safe_cast(List[str], params.get(PARAM_SEARCH_PATH))
        self.search_path.append(os.path.dirname(flow_runtime.config_path))

        # Handle context files
        if CONF_CONTEXT not in flow_runtime.flow_config:
            flow_runtime.flow_config[CONF_CONTEXT] = {}
        context_vars = flow_runtime.flow_config[CONF_CONTEXT]
        if not isinstance(context_vars, dict):
            raise ValueError("{} must be dictionary".format(CONF_CONTEXT))

        # Loading context files
        if CONF_CONTEXT_FILES in flow_runtime.flow_config:
            if not isinstance(flow_runtime.flow_config[CONF_CONTEXT_FILES], list):
                raise ValueError(
                    "{} must be a list".format(CONF_CONTEXT_FILES),
                )
            included_context: Dict[str, Any] = {}
            for context_file in flow_runtime.flow_config[CONF_CONTEXT_FILES]:
                ctx = yaml_file_to_dict(context_file)
                included_context = deepmerge_dict(included_context, ctx)
            context_vars = deepmerge_dict(included_context, context_vars)
            flow_runtime.context[RUNTIME_CONTEXT_VARS] = context_vars

        # Setup Jinja2
        self.__jinja_env = jinja2.Environment(
            comment_start_string="{##",
            comment_end_string="##}",
            loader=FileSystemLoader(searchpath=self.search_path, followlinks=True),
            **self.jinja_options,
        )

    def prepare_rendering_context(self, context: dict, flow_runtime: StromeRuntime):
        pass

    def run(self, flow_runtime: StromeRuntime):
        rendering_context = dict(
            config=flow_runtime.config,
            output=flow_runtime.context[RUNTIME_OUTPUT],
            build_time=datetime.datetime.now(),
        )
        self.prepare_rendering_context(rendering_context, flow_runtime)
        rendering_context.update(flow_runtime.context.get(RUNTIME_CONTEXT_VARS, {}))
        flow_runtime.context[RUNTIME_JINJA2_OUTPUT_FILES] = output_files = []
        for file_path in flow_runtime.flow_config.get(CONF_INPUT_FILES, tuple()):
            file_name = path.basename(file_path)
            output_file_path = path.join(self.output_dir, file_name)
            template = none_throws(self.__jinja_env).get_template(file_path, globals=rendering_context)  # type: ignore
            with open(output_file_path, "w") as f:
                f.write(template.render())
                output_files.append(output_file_path)
                flow_runtime.register_input_file(output_file_path)
