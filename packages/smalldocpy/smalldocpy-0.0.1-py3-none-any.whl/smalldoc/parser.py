# Copyright 2021 Jean-Pascal Thiery
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Parser read your module then extract data from source code and your docstring to build a dict.
"""
import pydoc
import inspect
import sys
import os
import re
from os.path import isdir, exists
import logging

logger = logging.getLogger(__name__)


def parse(working_path: str, module_name: str, show_private=False) -> dict:
    """
    Parse your code and  docstring then generate a dict with it.
    :param working_path: The working directory to fetch your module
    :param module_name: The name of the module you want to generate dict of your documentation
    :param show_private: If True, parser will navigate through your private methode. At False by default.
    :return: Dictionnary which contain metadata and doc.
    :rtype dict
    """
    logger.debug(f'loading path {working_path}')
    sys.path.append(working_path)
    try:
        mod = pydoc.safeimport(module_name)
        if mod is not None:
            return _parse_module(mod)
    except pydoc.ErrorDuringImport as e:
        logger.error(f'Error while trying to load module {module_name}: {e}')
        raise e


def _is_valid_module_name(module_name):
    return not module_name.startswith('.') \
           and not module_name.startswith('__')


def _get_sorted_value(item: dict) -> str:
    return item.get('name')


def _parse_module(module, show_private=False) -> dict:
    res = {
        'name': module.__name__,
        'description': _remove_first_and_last_newline(module.__doc__)
    }

    functions = [_parse_function(function) for function in inspect.getmembers(module, inspect.isfunction)
                 if not show_private and not function[0].startswith('_')]
    functions.sort(key=_get_sorted_value)
    res['functions'] = functions
    classes = [_parse_class(classe, show_private) for classe in inspect.getmembers(module, inspect.isclass)
               if not show_private and not classe[0].startswith('_')]
    classes.sort(key=_get_sorted_value)
    res['classes'] = classes

    modules = []
    module_path = os.path.dirname(os.path.abspath(module.__file__))
    for sub_module_path in [current_dir for current_dir in os.listdir(module_path) if
                            isdir(f'{module_path}/{current_dir}')
                            and _is_valid_module_name(current_dir)
                            and exists(f'{module_path}/{current_dir}/__init__.py')
                            ]:
        sub_module_name = f'{module.__name__}.{sub_module_path}'
        abs_sub_module_path = f'{module_path}/{sub_module_path}'
        sys.path.append(abs_sub_module_path)
        sub_mod = pydoc.safeimport(sub_module_name)
        modules.append(_parse_module(sub_mod))
    modules.sort(key=_get_sorted_value)
    res['modules'] = modules
    return res


def _parse_class(class_to_parse, show_private=False) -> dict:
    classe = class_to_parse[1]
    doc = inspect.getdoc(classe)
    nested_classes = [_parse_class(nested) for nested in inspect.getmembers(classe, inspect.isclass)
                      if nested[0] != "__class__" and not show_private and not nested[0].startswith('_')]
    nested_classes.sort(key=_get_sorted_value)
    functions = [_parse_function(function) for function in inspect.getmembers(classe, inspect.isfunction)
                 if not show_private and not function[0].startswith('_')]
    functions.sort(key=_get_sorted_value)
    return {
        'name': class_to_parse[0],
        'doc': _remove_first_and_last_newline(doc) if doc else '',
        'functions': functions,
        'classes': nested_classes
    }


def _parse_function(function_to_parse) -> dict:
    function = function_to_parse[1]
    args_spec = inspect.getfullargspec(function)
    signature = inspect.signature(function)
    doc = inspect.getdoc(function)

    def arg_doc(arg: str) -> str:
        arg_doc_res = ''
        match = re.search(rf':param[:]?\s*{arg}[:]?\s*([^\n]*)', doc) if doc else False
        if match:
            arg_doc_res = match.group(1)
        return arg_doc_res

    arguments = [{'name': arg,
                  'type': args_spec.annotations[arg].__name__ if arg in args_spec.annotations else '',
                  'doc': arg_doc(arg)
                  }
                 for arg in args_spec.args]
    if args_spec.varargs:
        arguments.append({
            'name': f'*{args_spec.varargs}',
            'type': '',
            'doc': ''
        })
    if args_spec.varkw:
        arguments.append({
            'name': f'**{args_spec.varkw}',
            'type': '',
            'doc': ''
        })

    arguments.sort(key=_get_sorted_value)
    return {
        'name': function_to_parse[0],
        'parameters': arguments,
        'return': _parse_return_function(function_to_parse),
        'def': f'def {function_to_parse[0]}{signature}',
        'doc': re.sub(r':\w.*((\n$)|$])?', '', doc) if doc else ''
    }


def _parse_return_function(function_to_parse) -> dict:
    function = function_to_parse[1]
    doc = pydoc.getdoc(function)
    signature = inspect.signature(function)
    return_type = ''
    return_type_class = signature.return_annotation
    if return_type_class == inspect._empty:
        # Extract from doc
        match = re.search(r':rtype[:]?\s*(\w*)', doc)
        if match:
            return_type = match.group(1)
    else:
        return_type = return_type_class.__name__
    return_doc = ''
    match_doc = re.search(r':return[:]?\s*([^\n]*)', doc)
    if match_doc:
        return_doc = _remove_first_and_last_newline(match_doc.group(1))
    return {
        'type': return_type,
        'doc': return_doc
    }


def _remove_first_and_last_newline(a_str: str) -> str:
    return re.sub(r'\n+$', '', re.sub(r'^\n+', '', a_str)) if a_str else ''
