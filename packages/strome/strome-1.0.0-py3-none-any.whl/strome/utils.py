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

import os
from typing import List, Optional

import yaml


def deepmerge_dict(full_old, full_new, merge_lists=False):
    def merge(old, new):
        # pylint: disable=no-else-return
        if isinstance(new, dict):
            if not isinstance(old, dict):
                return new
            res = old.copy()
            for k, v in new.items():
                res[k] = merge(old[k], v) if k in old else v
            return res
        elif isinstance(new, list):
            if merge_lists:
                if not isinstance(old, list):
                    return new
                return old + new
            else:
                return new
        return new

    return merge(full_old, full_new)


def yaml_file_to_dict(yaml_file: str) -> dict:
    with open(yaml_file, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def dict_to_yaml_file(yaml_dict: dict, yaml_file: str):
    with open(yaml_file, "w") as f:
        return yaml.dump(yaml_dict, f)


def get_all_existing_files(list_files: List[str]) -> List[str]:
    result = []
    for file_path in list_files:
        if os.path.exists(file_path):
            result.append(file_path)
    return result


def get_first_existing_file(list_files: List[str]) -> Optional[str]:
    res = get_all_existing_files(list_files)
    if len(res) == 0:
        return None
    return res[0]
