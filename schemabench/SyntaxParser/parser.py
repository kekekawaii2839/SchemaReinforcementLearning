from .base import BasicParser
from typing import Literal
import random
from .syntaxes import *
from .syntaxes import find_all_parser

class SyntaxesParser(BasicParser):
    """Union Syntaxes Parser for diverse syntaxes.
    
    Args
    ----
        default_parser (str): Set default parser for the union syntax parser.
        init_all_parser (bool): Whether init all possible parser writen in `.syntaxes`. This may take few times.
    
    Methods
    -------
        random() : return a random syntax parser
        all: return all parser class
    
    """
    
    def __init__(self, default_parser: Literal["json", "yaml", "toml", "xml", "hcl", "markdown"] = "json", init_all_parser: bool = False):
        super().__init__(default_parser)

        self.parsers: dict[str, BasicParser] = {}
        
        if init_all_parser:
            for parser in find_all_parser():
                try:
                    self.parsers[parser.__name__] = parser(parser.__name__)
                except:
                    pass
        

        self.default_parser = getattr(self, default_parser)
        
    def loads(self, s: str) -> dict:
        """Parse the given string and return the parsed data."""
        return self.default_parser.loads(s)
    
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return self.default_parser.dumps(obj)

    @property
    def all(self) -> tuple[BasicParser, ...]:
        """Return all syntax parsers."""
        return tuple(self.parsers.values())

    def random(self) -> BasicParser:
        """Return a random syntax parser."""
        return random.choice(self.all)

    def get(self, name: str) -> BasicParser:
        """Return the parser by the given name."""
        return self.parsers[name]
    
    
    
    @property
    def json(self):
        """Standard JSON Parser."""
        return StandardJsonParser("json")
    
    @property
    def yaml(self):
        """Standard YAML Parser."""
        return StandardYamlParser("yaml")
    
    @property
    def toml(self):
        """Standard TOML Parser."""
        return StandardTomlParser("toml")
    

    @property
    def xml(self):
        """Standard XML Parser."""
        return StandardXMLParser("xml")
    
    
    @property
    def hcl(self):
        """Standard HCL Parser."""
        return StandardHCLParser("hcl")
    
    @property
    def markdown(self):
        return KeyMarkdownParser("markdown")
    
    @property
    def csv(self):
        return StandardCSVParser("csv")
    
    @property
    def html(self):
        return StandardHTMLParser("html")
    
    @property
    def python(self):
        return StandardPythonParser("py")
    
    @property
    def sql(self):
        return SQLINSERTParser("sql")
    
    @property
    def plist(self):
        return StandardPlistParser("plist")