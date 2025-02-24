import tomli_w
import tomli
from typing import Any
from SyntaxParser.base import BasicParser

class StandardTomlParser(BasicParser):
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        return tomli.loads(s)
    
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return tomli_w.dumps(obj)
    
    