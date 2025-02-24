from typing import Any
from SyntaxParser.base import BasicParser
import json2html
from bs4 import BeautifulSoup,Tag

class StandardHTMLParser(BasicParser):
    """Standard HTML parser built with lib `json2html`.
    
    Note the `loads` methods may not work as expected, as the `json2html` library does not provide a way to convert the HTML back to JSON.
    """
    
    @property
    def intro(self):
        return "This is a special html syntax that represents the objects in a table format. All sub-objects are represented as sub-tables. List are represented as unordered lists."
    
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return json2html.json2html.convert(json = obj)
    
    def _parse_elem(self,elem:Tag):
        if elem.name == 'table':
            return self._parse_table(elem)
        if elem.name == 'ul':
            return self._parse_list(elem)
        if elem.name == 'li':
            return self._parse_item(elem)
        if elem.name == 'tr':
            return self._parse_row(elem)
        if elem.name == 'td':
            return self._parse_item(elem)
        return elem.text
    
    def _parse_table(self,elem:Tag):
        rows = elem.find_all('tr',recursive=False)
        result = {}
        for row in rows:
            key , value = self._parse_row(row)
            result[key] = value
        return result
    
    def _parse_list(self,elem:Tag):
        items = elem.find_all('li',recursive=False)
        result = []
        for item in items:
            result.append(self._parse_elem(item))
        return result
    
    def _parse_row(self,elem:Tag):
        return elem.find('th').text, self._parse_elem(elem.find('td'))
        
    
    def _parse_item(self,elem:Tag):
        if elem.find('table'):
            return self._parse_table(elem.find('table'))
        elif elem.find('ul'):
            return self._parse_list(elem.find('ul'))
        return elem.text
    
    
    def loads(self, s: str) -> Any:
        """Parse the given string and return the parsed data."""
        soup = BeautifulSoup(s, 'html.parser')
        
        return self._parse_elem(soup.find('table'))