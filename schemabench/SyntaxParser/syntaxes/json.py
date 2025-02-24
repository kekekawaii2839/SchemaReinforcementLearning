import os
import json
import re
from typing import Any
from SyntaxParser.base import BasicParser

class StandardJsonParser(BasicParser):
    
    def loads(self,s:str) -> Any:
        """Parse the given string and return the parsed data."""
        return json.loads(s)
    
    def dumps(self, obj: dict) -> str:
        """Convert the given object to string."""
        indent = os.environ.get('JSON_INDENT', None)
        if indent is not None:
            indent = int(indent)
        return json.dumps(obj,sort_keys=False,ensure_ascii=False,indent=indent)

class SparseJsonParser(StandardJsonParser):
    """Sparse json parser that set indent to 4"""
    def dumps(self, obj: dict) -> str:
        return json.dumps(obj,sort_keys=False,ensure_ascii=False,indent=4)

JSON_REGEX = r'```json\n(.*?)\n```'

class CodeBlockJsonParser(StandardJsonParser):
    """Parse JSON object contained in ```json\n \n```"""
    def loads(self, s: str) -> Any:
        re_res = re.search(JSON_REGEX, s, re.DOTALL)
        if re_res is not None:
            return super().loads(re_res.group(1))
        else:
            return super().loads(s)
    
    def dumps(self, obj: dict) -> str:
        s = super().dumps(obj)
        return "```json\n" + s + "\n```"

# custom loads function
from json5.lib import _walk_ast, _reject_duplicate_keys , Parser, Optional, Callable, Mapping, Any, Iterable, Tuple
from json5.parser import Parser

class CustomParser(Parser):
    def __init__(self, msg, fname, *, list_delimiters=None, object_delimiters=None, seperators=None):
        super().__init__(msg, fname)
        if list_delimiters:
            self._list_delimiters = list_delimiters
        else:
            self._list_delimiters = ('[', ']')
        if object_delimiters:
            self._object_delimiters = object_delimiters
        else:
            self._object_delimiters = ('{', '}')
        if seperators:
            self._seperators = seperators
        else:
            self._seperators = (',', ':')

    def _element_list__s1_l_p_(self):
        self._seq([self._sp_, lambda: self._ch(self._seperators[0]), self._sp_, self._value_])

    def _element_list__s3_(self):
        self._opt(lambda: self._ch(self._seperators[0]))

    def _member_list__s1_l_p_(self):
        self._seq([self._sp_, lambda: self._ch(self._seperators[0]), self._sp_, self._member_])

    def _member_list__s3_(self):
        self._opt(lambda: self._ch(self._seperators[0]))

    def _member__c0_(self):
        self._push('member__c0')
        self._seq(
            [
                lambda: self._bind(self._string_, 'k'),
                self._sp_,
                lambda: self._ch(self._seperators[1]),
                self._sp_,
                lambda: self._bind(self._value_, 'v'),
                lambda: self._succeed([self._get('k'), self._get('v')]),
            ]
        )
        self._pop('member__c0')

    def _member__c1_(self):
        self._push('member__c1')
        self._seq(
            [
                lambda: self._bind(self._ident_, 'k'),
                self._sp_,
                lambda: self._ch(self._seperators[1]),
                self._sp_,
                lambda: self._bind(self._value_, 'v'),
                lambda: self._succeed([self._get('k'), self._get('v')]),
            ]
        )
        self._pop('member__c1')

    def _array__c0_(self):
        self._push('array__c0')
        self._seq(
            [
                lambda: self._ch(self._list_delimiters[0]),
                self._sp_,
                lambda: self._bind(self._element_list_, 'v'),
                self._sp_,
                lambda: self._ch(self._list_delimiters[1]),
                lambda: self._succeed(self._get('v')),
            ]
        )
        self._pop('array__c0')

    def _array__c1_(self):
        self._seq(
            [
                lambda: self._ch(self._list_delimiters[0]),
                self._sp_,
                lambda: self._ch(self._list_delimiters[1]),
                lambda: self._succeed([]),
            ]
        )

    def _object__c0_(self):
        self._push('object__c0')
        self._seq(
            [
                lambda: self._ch(self._object_delimiters[0]),
                self._sp_,
                lambda: self._bind(self._member_list_, 'v'),
                self._sp_,
                lambda: self._ch(self._object_delimiters[1]),
                lambda: self._succeed(self._get('v')),
            ]
        )
        self._pop('object__c0')

    def _object__c1_(self):
        self._seq(
            [
                lambda: self._ch(self._object_delimiters[0]),
                self._sp_,
                lambda: self._ch(self._object_delimiters[1]),
                lambda: self._succeed([]),
            ]
        )

def loads(
    s: str,
    *,
    encoding: Optional[str] = None,
    cls: None = None,
    list_delimiters: Optional[Tuple[str,str]] = None,
    object_delimiters: Optional[Tuple[str,str]] = None,
    seperators: Optional[Tuple[str,str]] = None,
    object_hook: Optional[Callable[[Mapping[str, Any]], Any]] = None,
    parse_float: Optional[Callable[[str], Any]] = None,
    parse_int: Optional[Callable[[str], Any]] = None,
    parse_constant: Optional[Callable[[str], Any]] = None,
    object_pairs_hook: Optional[
        Callable[[Iterable[Tuple[str, Any]]], Any]
    ] = None,
    allow_duplicate_keys: bool = True,
):
    """Deserialize ``s`` (a string containing a JSON5 document) to a Python
    object.

    Supports the same arguments as ``json.load()`` except that:
        - the `cls` keyword is ignored.
        - an extra `allow_duplicate_keys` parameter supports checking for
          duplicate keys in a object; by default, this is True for
          compatibility with ``json.load()``, but if set to False and
          the object contains duplicate keys, a ValueError will be raised.
    """

    assert cls is None, 'Custom decoders are not supported'

    if isinstance(s, bytes):
        encoding = encoding or 'utf-8'
        s = s.decode(encoding)

    if not s:
        raise ValueError('Empty strings are not legal JSON5')
    if list_delimiters or object_delimiters or seperators:
        parser = CustomParser(s, '<string>', list_delimiters=list_delimiters, object_delimiters=object_delimiters, seperators=seperators)
    else:
        parser = Parser(s, '<string>')
    ast, err, _ = parser.parse()
    if err:
        raise ValueError(err)

    def _fp_constant_parser(s):
        return float(s.replace('Infinity', 'inf').replace('NaN', 'nan'))

    if object_pairs_hook:
        dictify = object_pairs_hook
    elif object_hook:

        def dictify(pairs):
            return object_hook(dict(pairs))
    else:
        dictify = dict

    if not allow_duplicate_keys:
        _orig_dictify = dictify

        def dictify(pairs):  # pylint: disable=function-redefined
            return _reject_duplicate_keys(pairs, _orig_dictify)

    parse_float = parse_float or float
    parse_int = parse_int or int
    parse_constant = parse_constant or _fp_constant_parser

    return _walk_ast(ast, dictify, parse_float, parse_int, parse_constant)

# custom dumps function
from json.encoder import (
    encode_basestring_ascii,
    encode_basestring,
    INFINITY,
)

class customJSONEncoder(json.JSONEncoder):
    def __init__(self, *, skipkeys=False, ensure_ascii=True,
            check_circular=True, allow_nan=True, sort_keys=False,
            indent=None, separators=None, list_delimiters=None, object_delimiters=None,default=None):
        super(customJSONEncoder, self).__init__(
            separators=separators,
            skipkeys=skipkeys, ensure_ascii=ensure_ascii,
            check_circular=check_circular, allow_nan=allow_nan, indent=indent,
            default=default, sort_keys=sort_keys)
        
        if separators is not None:
            self.item_separator, self.key_separator = separators
            if len(self.item_separator) == 1:
                self.item_separator = self.item_separator + ' '
            if len(self.key_separator) == 1:
                self.key_separator = self.key_separator + ' '
        elif indent is not None:
            self.item_separator, self.key_separator = separators
            self.item_separator = self.item_separator.strip()
            self.key_separator = self.key_separator.strip()

        if list_delimiters:
            self._list_delimiters = list_delimiters
        else:
            self._list_delimiters = ('[', ']')
        
        if object_delimiters:
            self._object_delimiters = object_delimiters
        else:
            self._object_delimiters = ('{', '}')
        
    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = encode_basestring_ascii
        else:
            _encoder = encode_basestring

        def floatstr(o, allow_nan=self.allow_nan,
                _repr=float.__repr__, _inf=INFINITY, _neginf=-INFINITY):
            # Check for specials.  Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on the
            # internals.

            if o != o:
                text = 'NaN'
            elif o == _inf:
                text = 'Infinity'
            elif o == _neginf:
                text = '-Infinity'
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError(
                    "Out of range float values are not JSON compliant: " +
                    repr(o))

            return text


        _iterencode = _make_iterencode(
            markers, self.default, _encoder, self.indent, floatstr,
            self.key_separator, self.item_separator, self.sort_keys,
            self.skipkeys, _one_shot,
            _object_delimiters=self._object_delimiters,
            _list_delimiters=self._list_delimiters,)
        return _iterencode(o, 0)
    
def _make_iterencode(markers, _default, _encoder, _indent, _floatstr,
        _key_separator, _item_separator, _sort_keys, _skipkeys, _one_shot,
        ## HACK: hand-optimized bytecode; turn globals into locals
        ValueError=ValueError,
        dict=dict,
        float=float,
        id=id,
        int=int,
        isinstance=isinstance,
        list=list,
        str=str,
        tuple=tuple,
        _intstr=int.__repr__,
        _list_delimiters=tuple,
        _object_delimiters=tuple,
    ):

    if _indent is not None and not isinstance(_indent, str):
        _indent = ' ' * _indent


    def _iterencode_list(lst, _current_indent_level):
        if not lst:
            yield f'{_list_delimiters[0]}{_list_delimiters[1]}'
            return
        if markers is not None:
            markerid = id(lst)
            if markerid in markers:
                raise ValueError("Circular reference detected")
            markers[markerid] = lst
        buf = f'{_list_delimiters[0]}'
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = '\n' + _indent * _current_indent_level
            separator = _item_separator + newline_indent
            buf += newline_indent
        else:
            newline_indent = None
            separator = _item_separator
        first = True
        for value in lst:
            if first:
                first = False
            else:
                buf = separator
            if isinstance(value, str):
                yield buf + _encoder(value)
            elif value is None:
                yield buf + 'null'
            elif value is True:
                yield buf + 'true'
            elif value is False:
                yield buf + 'false'
            elif isinstance(value, int):
                # Subclasses of int/float may override __repr__, but we still
                # want to encode them as integers/floats in JSON. One example
                # within the standard library is IntEnum.
                yield buf + _intstr(value)
            elif isinstance(value, float):
                # see comment above for int
                yield buf + _floatstr(value)
            else:
                yield buf
                if isinstance(value, (list, tuple)):
                    chunks = _iterencode_list(value, _current_indent_level)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value, _current_indent_level)
                else:
                    chunks = _iterencode(value, _current_indent_level)
                yield from chunks
        if newline_indent is not None:
            _current_indent_level -= 1
            yield '\n' + _indent * _current_indent_level
        yield _list_delimiters[1]
        if markers is not None:
            del markers[markerid]

    def _iterencode_dict(dct, _current_indent_level):
        if not dct:
            # yield '{}'
            yield f'{_object_delimiters[0]}{_object_delimiters[1]}'
            return
        if markers is not None:
            markerid = id(dct)
            if markerid in markers:
                raise ValueError("Circular reference detected")
            markers[markerid] = dct
        # yield '{'
        yield f'{_object_delimiters[0]}'
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = '\n' + _indent * _current_indent_level
            item_separator = _item_separator + newline_indent
            yield newline_indent
        else:
            newline_indent = None
            item_separator = _item_separator
        first = True
        if _sort_keys:
            items = sorted(dct.items())
        else:
            items = dct.items()
        for key, value in items:
            if isinstance(key, str):
                pass
            # JavaScript is weakly typed for these, so it makes sense to
            # also allow them.  Many encoders seem to do something like this.
            elif isinstance(key, float):
                # see comment for int/float in _make_iterencode
                key = _floatstr(key)
            elif key is True:
                key = 'true'
            elif key is False:
                key = 'false'
            elif key is None:
                key = 'null'
            elif isinstance(key, int):
                # see comment for int/float in _make_iterencode
                key = _intstr(key)
            elif _skipkeys:
                continue
            else:
                raise TypeError(f'keys must be str, int, float, bool or None, '
                                f'not {key.__class__.__name__}')
            if first:
                first = False
            else:
                yield item_separator
            yield _encoder(key)
            yield _key_separator
            if isinstance(value, str):
                yield _encoder(value)
            elif value is None:
                yield 'null'
            elif value is True:
                yield 'true'
            elif value is False:
                yield 'false'
            elif isinstance(value, int):
                # see comment for int/float in _make_iterencode
                yield _intstr(value)
            elif isinstance(value, float):
                # see comment for int/float in _make_iterencode
                yield _floatstr(value)
            else:
                if isinstance(value, (list, tuple)):
                    chunks = _iterencode_list(value, _current_indent_level)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value, _current_indent_level)
                else:
                    chunks = _iterencode(value, _current_indent_level)
                yield from chunks
        if newline_indent is not None:
            _current_indent_level -= 1
            yield '\n' + _indent * _current_indent_level
        # yield '}'
        yield f'{_object_delimiters[1]}'
        if markers is not None:
            del markers[markerid]

    def _iterencode(o, _current_indent_level):
        if isinstance(o, str):
            yield _encoder(o)
        elif o is None:
            yield 'null'
        elif o is True:
            yield 'true'
        elif o is False:
            yield 'false'
        elif isinstance(o, int):
            # see comment for int/float in _make_iterencode
            yield _intstr(o)
        elif isinstance(o, float):
            # see comment for int/float in _make_iterencode
            yield _floatstr(o)
        elif isinstance(o, (list, tuple)):
            yield from _iterencode_list(o, _current_indent_level)
        elif isinstance(o, dict):
            yield from _iterencode_dict(o, _current_indent_level)
        else:
            if markers is not None:
                markerid = id(o)
                if markerid in markers:
                    raise ValueError("Circular reference detected")
                markers[markerid] = o
            o = _default(o)
            yield from _iterencode(o, _current_indent_level)
            if markers is not None:
                del markers[markerid]
    return _iterencode



def json_parser_class_factory(class_name: str, list_delimiters=('[', ']'), object_delimiters=('{', '}'), separators=(', ', ': '), intro:str = ""):
    class CustomJsonParser(BasicParser):
        def __init__(self, name: str):
            super().__init__(name)
            self._list_delimiters = list_delimiters
            self._object_delimiters = object_delimiters
            self._separators = separators
            
        def loads(self,s:str) -> Any:
            """Parse the given string and return the parsed data."""
            return loads(s, list_delimiters=self._list_delimiters, object_delimiters=self._object_delimiters, seperators=self._separators)
        
        def dumps(self, obj: dict) -> str:
            """Convert the given object to string."""
            return json.dumps(obj,cls=customJSONEncoder,sort_keys=False,ensure_ascii=False,list_delimiters=self._list_delimiters,object_delimiters=self._object_delimiters,separators=self._separators)

        @property
        def intro(self):
            return intro

    CustomJsonParser.__name__ = class_name

    return CustomJsonParser

# DELIMITERS = [
#     ('<', '>'),
#     ('(', ')'),
#     ('【', '】'),
#     ('（', '）'),
#     ('「', '」'),
#     ('『', '』'),
# ]


JsonParsercl1 = json_parser_class_factory("JsonParsercl2", list_delimiters=('(', ')'), intro="Custom Json Syntax that replace object delimiters with '(' and ')'.")
JsonParsercl2 = json_parser_class_factory("JsonParsercl3", list_delimiters=('【', '】'), intro="Custom Json Syntax that replace object delimiters with '【' and '】'.")
JsonParsercl3 = json_parser_class_factory("JsonParsercl3", list_delimiters=('「', '」'), intro="Custom Json Syntax that replace object delimiters with '「' and '」'.")
JsonParsercl4 = json_parser_class_factory("JsonParsercl3", list_delimiters=('『', '』'), intro="Custom Json Syntax that replace object delimiters with '『' and '』'.")


JsonParserco1 = json_parser_class_factory("JsonParsercl2", object_delimiters=('<', '>'), intro="Custom Json Syntax that replace object delimiters with '<' and '>'.")
JsonParserco2 = json_parser_class_factory("JsonParsercl2", object_delimiters=('(', ')'), intro="Custom Json Syntax that replace object delimiters with '(' and ')'.")
JsonParserco3 = json_parser_class_factory("JsonParsercl2", object_delimiters=('【', '】'), intro="Custom Json Syntax that replace object delimiters with '【' and '】'.")
JsonParserco4 = json_parser_class_factory("JsonParsercl2", object_delimiters=('（', '）'), intro="Custom Json Syntax that replace object delimiters with '（' and '）'.")

# SEPARATORS = [
#     (';', ':'),
#     (';', '='),
#     ('、', '：'),
#     ('，', '：'),
#     ('，', '、'),
# ]

JsonParsercs1 = json_parser_class_factory("JsonParsercl2", separators=(';', ':'), intro="Custom Json Syntax that replace separators with ';' and ':'.")
JsonParsercs2 = json_parser_class_factory("JsonParsercl2", separators=(',', '='), intro="Custom Json Syntax that replace separators with ',' and '='.")
JsonParsercs3 = json_parser_class_factory("JsonParsercl2", separators=('、', '：'), intro="Custom Json Syntax that replace separators with '、' and '：'.")
JsonParsercs4 = json_parser_class_factory("JsonParsercl2", separators=(';', '='), intro="Custom Json Syntax that replace separators with ';' and '='.")

JsonParser1 = json_parser_class_factory("JsonParser1", list_delimiters=('「', '」'), object_delimiters=('<', '>'), separators=(';', '='), intro="Custom Json Syntax that replace object delimiters with '<' and '>', list delimiters with '「' and '」', separators with ';' and ':'.")
JsonParser2 = json_parser_class_factory("JsonParser2", list_delimiters=('『', '』'), object_delimiters=('【', '】'), separators=(';', ':'), intro="Custom Json Syntax that replace object delimiters with '【' and '】', list delimiters with '『' and '』', separators with ';' and ':'.")
JsonParser3 = json_parser_class_factory("JsonParser3", list_delimiters=('(', ')'), object_delimiters=('（', '）'), separators=('、', '：'), intro="Custom Json Syntax that replace object delimiters with '（' and '）', list delimiters with '(' and ')', separators with '、' and '：'.")