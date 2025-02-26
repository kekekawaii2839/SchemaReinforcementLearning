import yaml
import io
import os
from typing import Any
from SyntaxParser.base import BasicParser

class StandardYamlParser(BasicParser):
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        return yaml.load(io.StringIO(s),Loader=yaml.FullLoader)
    
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        sio = io.StringIO()
        yaml.dump(obj,sio,sort_keys=False,allow_unicode=True)
        s = sio.getvalue()
        sio.close()
        return s
    
class FlowYamlParser(BasicParser):
    
    @property
    def intro(self):
        return """This is a yaml parser that always use flow style."""
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        return yaml.load(io.StringIO(s),Loader=yaml.FullLoader)
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        sio = io.StringIO()
        yaml.dump(obj,sio,sort_keys=False,allow_unicode=True,default_flow_style=True)
        s = sio.getvalue()
        sio.close()
        return s

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap as OrderedDict
from ruamel.yaml.scalarstring import LiteralScalarString, DoubleQuotedScalarString
from ruamel.yaml.comments import CommentedSeq

class SimplifiedYamlParser(BasicParser):
    """This is add some customization for standard yaml to allow a better learn for language models, with the following features:
    
    - Always use double quoted string in the list.
    - Use flow style if the list is short.
    - Use literal style if the string contains '\n'.
    """
    @property
    def intro(self):
        return "This is a customized yaml parser that always use double quoted string in the list, use flow style if the list is short, and use literal style if the string contains '\\n'."
    
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        return yaml.load(io.StringIO(s),Loader=yaml.FullLoader)
    
    def dumps(self, obj: Any, width:int = 1000000) -> str:
        """Convert the given object to string."""
        def adjust_obj(obj:Any):
            if obj is None:
                return None
            elif isinstance(obj, dict):
                data = OrderedDict()
                for key in obj.keys():
                    data[key] = adjust_obj(obj[key])
                return data
            elif isinstance(obj,list):
                for idx in range(len(obj)):
                    if isinstance(obj[idx],str):
                        # always use double quoted string in the list
                        obj[idx] = DoubleQuotedScalarString(obj[idx])
                    else:
                        obj[idx] = adjust_obj(obj[idx])
                if sum([len(str(x)) for x in obj]) < 100:
                    # use flow style if the list is short
                    obj = CommentedSeq(obj)
                    obj.fa.set_flow_style()
                    return obj
            elif isinstance(obj, str):
                # if '\n' in obj:
                if os.environ.get('YAML_FORCE_LITERAL',"True") == 'True':
                    return LiteralScalarString(obj)
                else:
                    return DoubleQuotedScalarString(obj)
                # else:
                    # return obj
            else:
                return obj
            return obj
        
        dumper = ruamel.yaml.YAML()
        dumper.width = width
        map_indent = int(os.environ.get('YAML_MAP_INDENT',"2"))
        seq_indent = int(os.environ.get('YAML_SEQ_INDENT',"2"))
        offset = int(os.environ.get('YAML_OFFSET',"0"))
        dumper.indent(mapping=map_indent, sequence=seq_indent, offset=offset)
        sio = io.StringIO()
        dumper.dump(adjust_obj(obj),sio)
        s = sio.getvalue()
        return s