import csv
import io
from typing import Any
from SyntaxParser.base import BasicParser



class StandardCSVParser(BasicParser):
    """Standard Python Object to CSV covertor, using the csv module.
    
    Warning: only none nested object could be parsed!
    """
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        sio = io.StringIO(s)
        reader = csv.DictReader(sio)
        obj = next(reader)
        return obj
    
    def dumps(self, obj: Any) -> str:
        """Convert the given object to string."""
        # get fieldnames
        fieldnames = list(obj.keys())
        sio = io.StringIO()
        writer = csv.DictWriter(sio, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(obj)
        s = sio.getvalue()
        return s    
    
    
class FlattenCSVParser(BasicParser):
    """Flatten Python Object to CSV covertor, using the csv module."""
    
    @property
    def intro(self):
        return "This csv syntax should use special separator to flatten the nested structure."
    
    def dumps(self, obj: Any, sep: str = '::') -> str:
        """Convert the given object to string."""
        def flatten_dict(d, parent_key='',):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key).items())
                elif isinstance(v, (list, tuple, set)):
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            items.extend(flatten_dict(item, f"{new_key}{sep}{i}").items())
                        else:
                            items.append((f"{new_key}{sep}{i}", item))
                else:
                    items.append((new_key, v))
            return dict(items)
                
        _obj = flatten_dict(obj)
        
        sio = io.StringIO()
        writer = csv.DictWriter(sio, fieldnames=list(_obj.keys()))
        writer.writeheader()
        writer.writerow(_obj)
        s = sio.getvalue()
        return s
    
    def loads(self,s:str, sep = '::') -> Any:
        """Parse the given string and return the parsed data."""
        sio = io.StringIO(s)
        reader = csv.DictReader(sio)
        obj = next(reader)
        
        # recover the nested structure
        def recover(obj):
            new_obj = {}
            for k, v in obj.items():
                keys = k.split(sep)
                if len(keys) == 1:
                    new_obj[k] = v
                else:
                    _obj = new_obj
                    for key in keys[:-1]:
                        if key not in _obj:
                            _obj[key] = {}
                        _obj = _obj[key]
                    _obj[keys[-1]] = v
            return new_obj
        
        return recover(obj)