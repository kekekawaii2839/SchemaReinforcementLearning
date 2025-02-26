from abc import ABCMeta, abstractmethod
import jsonschema
from typing import Any
from .utils import get_complexity_obj,get_syntax_prompt,travese_and_convert
from .log import logger

class BasicParser(metaclass=ABCMeta):
    """Base Class for all parsers, each parser must inherit from this class."""
    
    def __init__(self,name:str):
        self.name = name
        self.logger = logger.getChild(name)
    
    @property
    def intro(self) -> str:
        """Return the introduction of the syntax."""
        return ""
        
    def get_random_obj(self,schema:dict) -> Any:
        """Generate a random object based on the schema."""
        return get_complexity_obj(schema,use_original_key=True)
    
    def check_schema(self,schema:dict) -> str:
        """Check if the given schema is valid for this syntax."""
        obj = get_complexity_obj(schema,use_original_key=True,raise_warning=True)
        sample_obj_str = self.dumps(obj)
        parsed_obj = self.loads(sample_obj_str)
        if parsed_obj == obj:
            return get_syntax_prompt(sample_obj_str,self.name) + '\n' + self.intro
        
        self.validate_loads(sample_obj_str,schema)
        
        return get_syntax_prompt(sample_obj_str,self.name) + '\n' + self.intro
        
    @abstractmethod
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        raise NotImplementedError
    
    @abstractmethod
    def dumps(self,obj:dict) -> str:
        """Convert the given object to string."""
        raise NotImplementedError
    
    def validate_loads(self, s: str, schema:dict) -> Any:
        """Validate the given string against the schema, return loaded object if valid."""
        obj = self.loads(s)

        try:
            jsonschema.validate(obj,schema)
        except jsonschema.ValidationError as e:
            # for bool, number, integer, None, we try to automatic convert them.
            obj = travese_and_convert(obj,schema)
            
            jsonschema.validate(obj,schema)
            self.logger.warning("Validation successed with automatic data type conversion. It is recommended to adjust the schema or user a more suitable syntax parser.")        

        return obj
    
    
    def validate_dumps(self, obj:dict, schema:dict) -> str:
        """Validate whether dumps are valid."""
        objstr = self.dumps(obj)
        obj2 = self.validate_loads(objstr, schema)
        if obj2 == obj:
            return objstr
        raise ValueError(f"Failed to validate dumps for object: {obj}. Loaded object: {obj2}")