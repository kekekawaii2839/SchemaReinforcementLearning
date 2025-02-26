import hcl2
from typing import Any
from SyntaxParser.base import BasicParser
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, TimeoutError

class StandardHCLParser(BasicParser):
    def __init__(self, name: str,timeout:int=1):
        super().__init__(name)
        self.timeout = timeout
        self.thdpool = ProcessPoolExecutor(max_workers=1)
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        # future = self.thdpool.submit(hcl2.loads, s)
        try:
            future = self.thdpool.submit(hcl2.loads, s)
            return future.result(timeout=self.timeout)
        except TimeoutError:
            for pid, process in self.thdpool._processes.items():
                process.terminate()
            self.thdpool.shutdown(wait=False)
            # for t in self.thdpool._threads:
            #     terminate_thread(t)
            return None

    
    def dumps(self, obj: dict|list, indent_level:int=0) -> str:
        """Convert the given object to string."""

        # TODO: Fix the extra newline with heredoc syntax
        hcl_str = ""
        indent = "  " * indent_level

        if isinstance(obj, dict):
            for key, value in obj.items():
                hcl_str += f'{indent}{key} = '
                if isinstance(value, (dict, list)):
                    hcl_str += '{\n' if isinstance(value, dict) else '[\n'
                    hcl_str += self.dumps(value, indent_level + 1)
                    hcl_str += f'\n{indent}' + ('}' if isinstance(value, dict) else ']')
                else:
                    # 处理基础数据类型
                    if isinstance(value, str):
                        # Escape quotes
                        # Check if the string contains newlines
                        if '\n' in value:
                            # If so, use heredoc syntax
                            hcl_str += f'<<EOT\n{value}\nEOT'
                        else:
                            escaped_value = value.replace('"', '\\"')
                            # Otherwise, just use a regular quoted string
                            hcl_str += f'"{escaped_value}"'
                    elif isinstance(value, bool):
                        hcl_str += 'true' if value else 'false'
                    elif value is None:
                        hcl_str += 'null'
                    else:
                        hcl_str += str(value)
                hcl_str += '\n'
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                if isinstance(item, (dict, list)):
                    hcl_str += indent + '{\n' if isinstance(item, dict) else indent + '[\n'
                    hcl_str += self.dumps(item, indent_level + 1)
                    hcl_str += f'\n{indent}' + ('}' if isinstance(item, dict) else ']')
                else:
                    # 处理基础数据类型
                    if isinstance(item, str):
                        # Escape quotes
                        # Check if the string contains newlines
                        if '\n' in item:
                            # If so, use heredoc syntax
                            hcl_str += f'<<EOT\n{item}\nEOT'
                        else:
                            escaped_value = item.replace('"', '\\"')
                            # Otherwise, just use a regular quoted string
                            hcl_str += f'"{escaped_value}"'
                    elif isinstance(item, bool):
                        hcl_str += indent + ('true' if item else 'false')
                    elif item is None:
                        hcl_str += indent + 'null'
                    else:
                        hcl_str += indent + str(item)
                if index < len(obj) - 1:
                    hcl_str += ','
                hcl_str += '\n'
        return hcl_str