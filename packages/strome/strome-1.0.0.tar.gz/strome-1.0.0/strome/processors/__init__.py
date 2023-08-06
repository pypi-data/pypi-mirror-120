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

from typing import Type, Optional, Dict, TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from strome.pipeline import PipelineElement


class PipelineElementRegistry(object):
    def __init__(self) -> None:
        self.__registry: Dict[str, Type[PipelineElement]] = {}

    def register(self, pipeline_element: Type["PipelineElement"], aliases: Optional[Sequence[str]] = None):
        self.__registry[pipeline_element.name()] = pipeline_element
        if aliases is not None:
            for alias in aliases:
                self.__registry[alias] = pipeline_element

    def get_by_name(self, name: str) -> Optional[Type["PipelineElement"]]:
        return self.__registry[name]

    def exists(self, name: str):
        return name in self.__registry


REGISTRY = PipelineElementRegistry()
