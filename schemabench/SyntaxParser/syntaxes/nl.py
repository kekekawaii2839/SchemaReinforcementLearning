from typing import Any
import re
from SyntaxParser.base import BasicParser

class GSMNLParser(BasicParser):
    """GSMNLParser is a parser for the GSMNL format.
    
    Only support GSM NL format as follow:
    
    ```
    {thought}#### {answer}
    ```
    """
    
    @property
    def intro(self):
        return "This GSM NL format is a simple format that contains the thought and answer separated by '####'."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        """
        m = re.match(r"(.*)#### (.*)", s, re.DOTALL).groups()
        return {
            "thought": m[0].strip(),
            "answer": float(m[1].replace(",", "")) if m[1] != "None" else None
        }

    
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['thought']}#### {obj['answer']}"

class LLAMA3_1NLParser(BasicParser):
    """LLAMA3_1NLParser only support the following format:
    
    ```
    {thought}$\\boxed\{{answer}\}$
    ```
    """
    @property
    def intro(self):
        return "This LLAMA3.1 NL format is a simple format that contains the thought and answer separated by '$\\boxed{answer}$'."

    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        """
        m = re.match(r"(.*)\$\\boxed\{(.*)\}\$$", s, re.DOTALL).groups()
        return {
            "thought": m[0],
            "answer": float(m[1].replace(",", "")) if m[1] != "None" else None
        }

    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['thought']}$\\boxed"+"{"+str(obj['answer'])+"}$"

class BBHNLParser(BasicParser):
    """BBHNLParser only support answers for BBH:
    
    ```
    {thought} So the answer is {answer}.
    ```
    """
    @property
    def intro(self):
        return "This BBH dataset format is a simple format that contains the thought and answer. You should give your answer in the last sentence, like \"So the answer is {answer}.\""

    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        """
        m = re.match(r"(.*)So the answer is (.*).$", s, re.DOTALL).groups()
        ans = m[1].replace(",", "")
        if ans == "True":
            ans = True
        elif ans == "False":
            ans = False
        else:
            try:
                ans = float(ans)
            except:
                pass
        return {
            "thought": m[0],
            "answer": ans
        }

    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['thought']} So the answer is {obj['answer']}."


class MATHNLParser(BasicParser):
    @property
    def intro(self):
        return "This MATH NL format is a simple format that contains the thought and answer separated by last `$\\boxed{{answer}}$`."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        Only support MATH NL format as follow:
        {thought}$\\boxed{{{answer}}}$
        """
        answer = self.remove_boxed(self.last_boxed_only_string(s))
        thought = s.rsplit(f"$\\boxed{{{answer}}}$", 1)
        thought = "".join(thought)
        return {"thought": thought, "answer": answer}

    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['thought']}$\\boxed{{{obj['answer']}}}$"

    def last_boxed_only_string(self, string):
        idx = string.rfind("\\boxed")
        if idx < 0:
            idx = string.rfind("\\fbox")
            if idx < 0:
                return None

        i = idx
        right_brace_idx = None
        num_left_braces_open = 0
        while i < len(string):
            if string[i] == "{":
                num_left_braces_open += 1
            if string[i] == "}":
                num_left_braces_open -= 1
                if num_left_braces_open == 0:
                    right_brace_idx = i
                    break
            i += 1
        
        if right_brace_idx == None:
            retval = None
        else:
            retval = string[idx:right_brace_idx + 1]
        
        return retval

    def remove_boxed(self, s):
        left = "\\boxed{"
        try:
            assert s[:len(left)] == left
            assert s[-1] == "}"
            return s[len(left):-1]
        except:
            return None
    

class TheoremQANLParser(BasicParser):
    @property
    def intro(self):
        return "This TheoremQA NL format is a simple format that contains the thought and answer separated by '\nThe answer is '."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        Only support TheoremQA NL format as follow:
        {thought}\nThe answer is {answer}
        """
        match = re.match(r"(.*)\nThe answer is (.*).", s, re.DOTALL)
        if match:
            return {
                "thought": match.group(1),
                "answer": match.group(2)
            }

    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['thought']}\nThe answer is {obj['answer']}."
    

class SVAMPNLParser(BasicParser):
    @property
    def intro(self):
        return "This SVAMP NL format is a simple format that contains the thought and answer separated by '\n####'."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        Only support SVAMP NL format as follow:
        {thought}\n#### {answer}
        """
        match = re.match(r"(.*)\n#### (.*)", s, re.DOTALL)
        if match:
            return {
                "thought": match.group(1),
                "answer": float(match.group(2))
            }

    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['thought']}\n#### {obj['answer']}"
    

class CodeNLParser(BasicParser):
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        Only support HumanEval NL format as follow:
        {code}
        """
        return {"code": s}

    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['code']}"
    

class MMLUNLParser(BasicParser):
    @property
    def intro(self):
        return "This MMLU NL format is a simple format that contains the thought and answer separated by '\nSo the answer is: '."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        Only support MMLU NL format as follow:
        {thought}\nSo the answer is: {answer}
        """
        match = re.match(r"(.*)\nSo the answer is: (.*).", s, re.DOTALL)
        if match:
            return {
                "thought": match.group(1),
                "answer": match.group(2)
            }

    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['thought']}\nSo the answer is: {obj['answer']}."
    

class ARCNLParser(BasicParser):
    @property
    def intro(self):
        return "This ARC NL format is a simple format that contains the thought and answer separated by '\nSo the answer is: '."
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data.
        Only support MMLU NL format as follow:
        {thought}\nSo the answer is: {answer}
        """
        match = re.match(r"(.*)\nSo the answer is: (.*).", s, re.DOTALL)
        if match:
            return {
                "thought": match.group(1),
                "answer": match.group(2)
            }

    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        return f"{obj['thought']}\nSo the answer is: {obj['answer']}."