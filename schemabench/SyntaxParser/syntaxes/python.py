from typing import Any
from SyntaxParser.base import BasicParser


class StandardPythonParser(BasicParser):
    """Standard Python Object to Python code covertor, using the repr function."""
    
    @property
    def intro(self) -> str:
        return "This syntax is designed to parse a simple python object to python code."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        obj = eval(s,{})
        return obj
    
    def dumps(self, obj: Any) -> str:
        """Convert the given object to string."""
        s = repr(obj)
        return s
    

class PydanticParser(BasicParser):
    """Read/Write the object in pydantic code format."""
    