from typing import Any
from SyntaxParser.base import BasicParser


class KeyMarkdownParser(BasicParser):
    
    # TODO: Use lib mistune to parse the markdown    
    @property
    def intro(self) -> str:
        return "This syntax is designed to parse a simple markdown syntax that uses outlines as keys and the following lines as values. Numbers should be enclosed in two backticks (`) characters."
    
    def _parse_dict(self):
        result = {}
        while self.idx < len(self.lines):
            line = self.lines[self.idx]
            # first check the control characters
            if line.startswith('#'):
                level = line.count('#')
                key = line[level:].strip()
                self.idx += 1
                if self.clevel == level:
                    # extract value
                    value = self._parse_value(self.lines[self.idx])
                    while self.idx < len(self.lines) and not (self.lines[self.idx].startswith('#') or self.lines[self.idx].startswith('-') or self.lines[self.idx].startswith('`')):
                        value += '\n' + self._parse_value(self.lines[self.idx])
                    
                    result[key] = value
                elif self.clevel < level:
                    # parse as dict
                    self.clevel = level
                    value = self._parse_dict()
                    
                    result[key] = value
                else:
                    return result
            elif line.startswith('-'):
                # parse as list
                value = self._parse_list()
                return value
            else:
                raise ValueError(f'Invalid line: {line}')
        return result
    
    def _parse_list(self) -> list:
        result = []
        while self.idx < len(self.lines):
            line = self.lines[self.idx]
            if line.startswith('-'):
                value = self._parse_value(line[1:])
                result.append(value)
            else:
                return result
        return result
    
    def _parse_value(self,line:str):
        if line.startswith('-'):
            return self._parse_list()
        if line.startswith('#'):
            return self._parse_dict()
        if line.startswith('`') and line.endswith('`'):
            self.idx += 1
            if '.' in line:
                return float(line[1:-1])
            return int(line[1:-1])   
        self.idx += 1
        return line
    
    def _parse(self):
        return self._parse_dict()
    
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        
        This will parse outlines as dict key.
        Example:
        # Key1
        value
        
        ## Key1.1
        - value
        - value
        
        # Key2
        aacbbb `123`
        
        ====>
        
        {
            'key1': {
                'key1.1':[
                    'value',
                    'value'
                ]
            },
            'key2': 123
        }
        """
        self.lines =  s.split('\n')
        self.lines = [line for line in self.lines]
        self.idx = 0
        self.clevel = 1
        return self._parse()
    
    def dumps(self, obj: dict|list|int|float|tuple|str|None,indent:int=1) -> str:
        """Convert the given object to string."""
        if obj is None:
            return 'None'
        if isinstance(obj, (int,float)):
            return f'`{str(obj)}`'
        if isinstance(obj,str):
            return obj
        if isinstance(obj, list):
            return '\n- ' + '\n- '.join(self.dumps(item,indent) for item in obj) + '\n'
        if isinstance(obj, dict):
            starts = '#'*indent
            return '\n'.join(f'{starts} {key}\n{self.dumps(value,indent=indent+1)}' for key,value in obj.items())
        raise ValueError(f'Unsupported type: {type(obj)}')
    