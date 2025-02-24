from typing import Any
from SyntaxParser.base import BasicParser
import json
import re


class SQLINSERTParser(BasicParser):
    """SQL INSERT parser that convert object into SQL INSERT statement."""
    
    @property
    def intro(self):
        return "This is a SQL INSERT syntax that convert object into SQL INSERT statement. Multiple string should use '\\n' as line break. Nested Object should be converted into JSON string. Array should be converted into ARRAY[]."
    
    def dumps(self, obj: Any, table: str = "root") -> str:
        def python2sql(value):
            if isinstance(value, str):
                value = value.replace('\n','\\n').replace("'","\\'")
                return f"'{value}'"
            elif isinstance(value, (int, float)):
                return str(value)
            elif isinstance(value, list):
                return f"ARRAY[{', '.join(python2sql(v) for v in value)}]"
            elif isinstance(value, dict):
                return f"'{json.dumps(value)}'"
            elif value is None:
                return 'NULL'
            else:
                raise TypeError(f"Unsupported type: {type(value)}")
        
        columns = ', '.join(obj.keys())
        values = ', '.join(python2sql(value) for value in obj.values())
        return f"INSERT INTO {table} ({columns}) VALUES ({values});"
    
    def loads(self, s: str) -> Any:
        table,columns,values = re.match(r"INSERT INTO (.*) \((.*)\) VALUES \((.*)\);",s,re.DOTALL).groups()
        columns = columns.split(', ')
        
        
        class convert:
            def __getitem__(self,key):
                return list(key)
        
        g = {
            'ARRAY': convert()
        }
        
        values = eval(f'[{values}]',g)
        result = {}
        for k,v in zip(columns,values):
            result[k] = v
            if isinstance(result[k],str):
                try:
                    result[k] = json.loads(result[k])
                    if isinstance(result[k],str):
                        result[k] = result[k].replace('\\n','\n').replace("\\'","'")
                except:
                    pass
        return result
        

class SQLUPDATEParser(BasicParser):
    """SQL UPDATE parser that convert object into SQL UPDATE statement."""

    @property
    def intro(self):
        return "This is a SQL UPDATE syntax that convert object into SQL UPDATE statement. Multiple string should use '\\n' as line break. Nested Object should be converted into JSON string. Array should be converted into ARRAY[]."
    

    def dumps(self,obj:dict, table:str = 'root'):
        def python2sql(value):
            if isinstance(value, str):
                value = value.replace('\n','\\n')
                return f"'{value}'"
            elif isinstance(value, (int, float)):
                return str(value)
            elif isinstance(value, list):
                return f"ARRAY[{', '.join(python2sql(v) for v in value)}]"
            elif isinstance(value, dict):
                return f"'{json.dumps(value,ensure_ascii=False)}'"
            elif value is None:
                return 'NULL'
            else:
                raise TypeError(f"Unsupported type: {type(value)}")
        
        sets = ', '.join([f"{k} = {python2sql(v)}" for k,v in obj.items()])
        return f"UPDATE {table} SET {sets};"
    
    def loads(self,s:str) -> Any:
        table,sets = re.match(r"UPDATE (.*) SET (.*);",s,re.DOTALL).groups()

        # extract each set value
        pattern = re.compile(r'(\w+)\s*=\s*(ARRAY\[.*?\]|\'[^\']*\'|\{[^\}]*\}|\d+|NULL)', re.DOTALL)
        sets = pattern.findall(sets)
        
        class convert:
            def __getitem__(self,key):
                return list(key)
        
        g = {
            'ARRAY': convert()
        }
        for s in sets:
            exec(f'{s[0]} = {s[1]}',g)
        for k,v in g.items():
            if isinstance(v,str):
                try:
                    g[k] = json.loads(v)
                    if isinstance(g[k],str):
                        g[k] = g[k].replace('\\n','\n')
                except:
                    pass
        
        g.pop('ARRAY')
        g.pop('__builtins__')
        return g