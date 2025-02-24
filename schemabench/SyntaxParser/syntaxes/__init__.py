from .json import StandardJsonParser,SparseJsonParser,json_parser_class_factory
from .yaml import StandardYamlParser,FlowYamlParser,SimplifiedYamlParser
from .toml import StandardTomlParser
from .xml import StandardXMLParser,StandardPlistParser
from .hcl import StandardHCLParser
from .markdown import KeyMarkdownParser
from .csv import StandardCSVParser,FlattenCSVParser
from .html import StandardHTMLParser
from .python import StandardPythonParser
from .sql import SQLINSERTParser,SQLUPDATEParser

__all__ = [
    "StandardJsonParser","SparseJsonParser","json_parser_class_factory",
    "StandardYamlParser","FlowYamlParser","SimplifiedYamlParser",
    "StandardTomlParser",
    "StandardXMLParser","StandardPlistParser","StandardHTMLParser",
    "StandardHCLParser",
    "KeyMarkdownParser",
    "StandardCSVParser","FlattenCSVParser",
    "StandardPythonParser",
    "SQLINSERTParser","SQLUPDATEParser"
    ]

from ..base import BasicParser

import os
import inspect
import importlib.util

def find_subclasses_in_file(file_path, base_class):
    subclasses = []
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, base_class) and obj is not base_class:
            subclasses.append(obj)
    return subclasses

def find_all_parser(directory = None, base_class = BasicParser) -> list[BasicParser]:
    all_subclasses = []
    if directory is None:
        directory = os.path.dirname(__file__)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                subclasses = find_subclasses_in_file(file_path, base_class)
                all_subclasses.extend(subclasses)
    return all_subclasses