from typing import Any
from SyntaxParser.base import BasicParser
import xmltodict
import plistlib
import io

class StandardXMLParser(BasicParser):
    
    @property
    def intro(self) -> str:
        return "This xml syntax is designed to parse objects. Set key as the tag name and value as the text content."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        return xmltodict.parse(s,process_namespaces=False,process_comments=True)["root"]
    
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return xmltodict.unparse({"root":obj},pretty=True)
    

class StandardPlistParser(BasicParser):
    
    @property
    def intro(self) -> str:
        return "This plist syntax is designed to parse objects. Follow the APLLE.INC plist format."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        return plistlib.loads(s.encode("utf-8"))
    
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return plistlib.dumps(obj,sort_keys=False).decode("utf-8")