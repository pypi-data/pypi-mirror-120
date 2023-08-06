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

from typing import Optional, TYPE_CHECKING

from cli_rack_validation.domain import ValidationResult

if TYPE_CHECKING:
    from strome.pipeline import PipelineElement


class BaseStromeError(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)


class ProcessorLoadingError(BaseStromeError):
    def __init__(self, message, processor_cls: "PipelineElement" = None, recommendation: str = None) -> None:
        super().__init__(message, processor_cls, recommendation=recommendation)


class ConfigValidationError(BaseStromeError):
    def __init__(
        self,
        message,
        processor_cls: Optional["PipelineElement"] = None,
        validation_result: Optional["ValidationResult"] = None,
        recommendation: Optional[str] = None,
        config_section: Optional[str] = None,
    ) -> None:
        super().__init__(
            message,
            processor_cls,
            config_section=config_section,
            validation_result=validation_result,
            recommendation=recommendation,
        )


class InvalidModuleError(BaseStromeError):
    pass


class ProcessorRuntimeError(BaseStromeError):
    pass
