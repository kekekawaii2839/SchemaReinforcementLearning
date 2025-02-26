import json
from .log import logger
letters = "abcdefghijklmnopqrstuvwxyz"
normalized_keys: list[str] = [a+b for a in letters for b in letters]


def get_syntax_prompt(sample_obj_str:str,syntax_name:str = "") -> str:
    return f"You should generate answer with following {syntax_name} format:\n{sample_obj_str}"

def get_char_complexity(obj,) -> int:
    s = json.dumps(obj)
    return len(s)

class SchemaObjectError(Exception):
    pass


def travese_and_convert(obj,schema):
    """Try to automatically convert boolean, number, integer, null."""
    if "type" in schema:
        match schema["type"]:
            case "object":
                newobj = {}
                if "properties" in schema:
                    for key in schema["properties"]:
                        newobj[key] = travese_and_convert(obj[key],schema["properties"][key])
                if "patternProperties" in schema:
                    for key in schema["patternProperties"]:
                        newobj[key] = travese_and_convert(obj[key],schema["patternProperties"][key])
                if "maxProperties" in schema:
                    raise NotImplementedError
                return newobj
            case "array":
                arr = []
                if "items" in schema:
                    try:
                        iter(schema["items"])
                        # multiple items mixed schema
                        for item in obj:
                            valid = False
                            for subschema in schema["items"]:
                                try:
                                    arr.append(travese_and_convert(item,subschema))
                                    valid = True
                                    break
                                except:
                                    pass
                            if not valid:
                                # main original obj
                                arr.append(item)
                        
                    except:
                        for item in obj:
                            arr.append(travese_and_convert(item,schema["items"]))
                            
                return arr
            case "string":
                return str(obj)
            case "number":
                try:
                    return int(obj)
                except:
                    return float(obj)
            case "integer":
                return int(obj)
            case "boolean":
                if isinstance(obj,bool):
                    return obj
                if isinstance(obj,str):
                    if obj.lower() == "true":
                        return True
                    if obj.lower() == "false":
                        return False
                    raise ValueError(f"Invalid boolean value {obj}")
                return bool(obj)

            case "null":
                if isinstance(obj,str):
                    if obj.lower() == "null" or obj == "" or obj == "None":
                        return None
                    raise ValueError(f"Invalid null value {obj}")
                return obj
            
            case _:
                return obj
    else:
        if "allOf" in schema:
            for subschema in schema["allOf"]:
                obj = travese_and_convert(obj,subschema)
            return obj
        elif "anyOf" in schema:
            for subschema in schema["anyOf"]:
                try:
                    return travese_and_convert(obj,subschema)
                except:
                    pass
            return obj
        elif "oneOf" in schema:
            for subschema in schema["oneOf"]:
                try:
                    return travese_and_convert(obj,subschema)
                except:
                    pass
            return obj
        else:
            return obj


def get_complexity_obj(schema: object, use_original_key=False, raise_warning:bool = False) -> dict:
    # assert "type" in schema, "type is required"
    if "type" in schema:
        match schema["type"]:
            case "object":
                obj = {}
                idx = 0
                # warning: max support 676 properties
                if "properties" in schema:
                    for key, value in schema["properties"].items():
                        obj[normalized_keys[idx]if not use_original_key else key] = get_complexity_obj(
                            value, use_original_key=use_original_key,raise_warning=raise_warning)
                        idx += 1
                if "patternProperties" in schema:
                    for key, value in schema["patternProperties"].items():
                        obj[normalized_keys[idx]if not use_original_key else key] = get_complexity_obj(
                            value, use_original_key=use_original_key,raise_warning=raise_warning)
                        idx += 1
                if "maxProperties" in schema:
                    complexities = [
                        (k, get_char_complexity(obj)) for k in obj.keys()
                    ]
                    sorted(complexities, key=lambda x: x[1])
                    newobj = {k: v for k, v in obj.items() if k in [
                        x[0] for x in complexities[:schema["maxProperties"]]]}
                    obj = newobj

                return obj

            case "array":
                arr = []                    
                if "contains" in schema:
                    arr.append(get_complexity_obj(
                        schema["contains"], use_original_key=use_original_key,raise_warning=raise_warning))

                if "items" in schema:
                    num_objs = schema.get("minItems",0) - len(arr)
                    try:
                        assert not isinstance(schema["items"],dict), "items should be a list"
                        iter(schema["items"])                      
                        
                        for idx in range(0,num_objs):
                            arr.append(get_complexity_obj(schema=schema['items'][idx%len(schema['items'])],use_original_key=use_original_key,raise_warning=raise_warning))

                    except:
                        child_complexity = get_complexity_obj(
                            schema['items'], use_original_key=use_original_key,raise_warning=raise_warning)
                        
                        for idx in range(0,num_objs):
                            arr.append(child_complexity)

                return arr

            case "string":
                s = ""
                if "description" in schema:
                    s += schema["description"]
                if "pattern" in schema:
                    # if raise_warning:
                    #     raise SchemaObjectError("pattern is not supported!")
                    # else:
                    logger.warning("Pattern is not supported and will be ignored!")
                if "minLength" in schema and len(s) < schema["minLength"]:
                    s += " " * schema["minLength"]
                return s
            case "number" | "integer":
                n = 0

                if "minimum" or "exclusiveMinimum" in schema:
                    if "maximum" or "exclusiveMaximum" in schema:
                        if "exclusiveMaximum" in schema and schema["exclusiveMaximum"] < 0:
                            n = schema["exclusiveMaximum"] - 1
                        elif "maximum" in schema and schema["maximum"] < 0:
                            n = schema["maximum"]
                        else:
                            if "minimum" in schema and schema["minimum"] > 0:
                                n = schema["minimum"]
                            elif "exclusiveMinimum" in schema and schema["exclusiveMinimum"] > 0:
                                n = schema["exclusiveMinimum"] + 1
                            else:
                                n = 0
                    else:
                        if "minimum" in schema and schema["minimum"] > 0:
                            n = schema["minimum"]
                        elif "exclusiveMinimum" in schema and schema["exclusiveMinimum"] > 0:
                            n = schema["exclusiveMinimum"] + 1
                        else:
                            n = 0
                else:
                    if "maximum" or "exclusiveMaximum" in schema:
                        if "exclusiveMaximum" in schema and schema["exclusiveMaximum"] < 0:
                            n = schema["exclusiveMaximum"] - 1
                        elif "maximum" in schema and schema["maximum"] < 0:
                            n = schema["maximum"]
                        else:
                            n = 0
                    else:
                        n = 0

                if "multipleOf" in schema:
                    # round n to the nearest multiple of multipleOf
                    n = n - n % schema["multipleOf"]

                return n

            case "boolean":
                return True
            case "null":
                return None
            case _:
                raise SchemaObjectError(f"Unsupported type: {schema['type']}")
    else:
        if "const" in schema:
            return schema["const"]
        elif "enum" in schema:
            complexities = [get_char_complexity(
                item) for item in schema["enum"]]
            return schema["enum"][complexities.index(max(complexities))]
        else:
            if "allOf" in schema:
                logger.warning("allOf is not supported and may cause unexpected results!")
                # construct new schema
                new_schema = {}
                for item in schema["allOf"]:
                    new_schema.update(item)
                return get_complexity_obj(new_schema, use_original_key=use_original_key,raise_warning=raise_warning)
            elif "anyOf" in schema:
                logger.warning("anyOf is not supported and may cause unexpected results!")
                objs = [get_complexity_obj(item, use_original_key=use_original_key,raise_warning=raise_warning) for item in schema["anyOf"]]
                complexities = [get_char_complexity(
                    item) for item in objs]
                return objs[complexities.index(max(complexities))]
            elif "oneOf" in schema:
                logger.warning("oneOf is not supported and may cause unexpected results!")
                objs = [get_complexity_obj(item, use_original_key=use_original_key,raise_warning=raise_warning) for item in schema["oneOf"]]
                complexities = [get_char_complexity(
                    item) for item in objs]
                return objs[complexities.index(max(complexities))]
            elif "not" in schema:
                if raise_warning:
                    raise SchemaObjectError("not is not supported!")
                else:
                    logger.warning("not is not supported and will be ignored!")
            elif "$ref" in schema:
                if raise_warning:
                    raise SchemaObjectError("$ref is not supported!")
                else:
                    logger.warning("$ref is not supported and will be ignored!")
            else:
                raise SchemaObjectError(f"Unsupported schema {schema}!")



if __name__ == "__main__":

    # Prompt: history tool call
    # assistant: thought and tool call in syntax (JSON/YAML/...)

    schema = {'type': 'object',
 'properties': {'content': {'description': 'Anything that is helpful to you.',
   'type': 'string'},
  'observation': {'description': 'What do you think about the things you observed. Around 50 words.',
   'type': 'string'},
  'thought': {'description': 'What to do next, learn from the former results and correct your action. Around 50 words.',
   'type': 'string'},
  'criticism': {'description': 'as a super agent, constructive self-criticism of the current thought and plan on its weakness and strength.',
   'type': 'string'},
  'thoughts':{
    'type': 'array',
    'contains': {'type': 'string'},
    'minItems': 1,
    'maxItems': 3,
    'items':[
        {'type':'string'},
        {'type': 'number'}
    ]
  },
  'tool_call': {'oneOf': [{'type': 'object',
     'description': 'Creates a personalized storybook for a user.\n\nArgs:\n    user_name (str): The name of the user.\n    user_age (int): The age of the user.\n    user_traits (List[str]): List of traits possessed by the user.\n\nReturns:\n    Storybook: The personalized storybook created for the user.',
     'properties': {'name': {'const': 'create_personalized_storybook'},
      'arguments': {'type': 'object',
       'properties': {'user_name': {'title': 'User Name', 'type': 'string'},
        'user_age': {'title': 'User Age', 'type': 'integer'},
        'user_traits': {'title': 'User Traits',
         'type': 'array',
         'items': {'type': 'string'}}},
       'required': ['user_name', 'user_age', 'user_traits']}}},
    {'type': 'object',
     'description': 'Retrieves a user by user_id.\n\nArgs:\n    user_id (int): The unique identifier of the user.\n\nReturns:\n    User: The user object.',
     'properties': {'name': {'const': 'get_user'},
      'arguments': {'type': 'object',
       'properties': {'user_id': {'title': 'User Id', 'type': 'integer'}},
       'required': ['user_id']}}},
    {'type': 'object',
     'description': 'Retrieves the user information for a given user ID.\n\nArgs:\n    user_id (str): The unique identifier for the user.\n\nReturns:\n    UserInfo: The user information.',
     'properties': {'name': {'const': 'get_user_info'},
      'arguments': {'type': 'object',
       'properties': {'user_id': {'title': 'User Id', 'type': 'string'}},
       'required': ['user_id']}}},
    {'type': 'object',
     'description': 'Returns a list of users for user demo.\n\nArgs:\n    user (User): The user for demo.\n\nReturns:\n    List[User]: The list of users for user demo.',
     'properties': {'name': {'const': 'get_users_for_user_demo'},
      'arguments': {'type': 'object',
       'properties': {'user': {'title': 'User',
         'type': 'object',
         'properties': {'user_id': {'title': 'User Id',
           'description': 'The unique identifier for a user',
           'default': 0,
           'type': 'integer'},
          'name': {'title': 'Name',
           'description': 'The name of the user',
           'type': 'string'},
          'email': {'title': 'Email',
           'description': 'The email address of the user',
           'type': 'string'},
          'phone': {'title': 'Phone',
           'description': 'The phone number of the user',
           'type': 'string'},
          'address': {'title': 'Address',
           'description': 'The address of the user',
           'allOf': [{'title': 'Address',
             'type': 'object',
             'properties': {'street': {'title': 'Street',
               'description': 'The street address',
               'type': 'string'},
              'city': {'title': 'City',
               'description': 'The city',
               'type': 'string'},
              'state': {'title': 'State',
               'description': 'The state',
               'type': 'string'}},
             'required': ['street', 'city', 'state']}]},
          'company': {'title': 'Company',
           'description': 'The company the user is affiliated with',
           'allOf': [{'title': 'Company',
             'type': 'object',
             'properties': {'name': {'title': 'Name',
               'description': 'The name of the company',
               'type': 'string'},
              'address': {'title': 'Address',
               'description': 'The address of the company',
               'allOf': [{'title': 'Address',
                 'type': 'object',
                 'properties': {'street': {'title': 'Street',
                   'description': 'The street address',
                   'type': 'string'},
                  'city': {'title': 'City',
                   'description': 'The city',
                   'type': 'string'},
                  'state': {'title': 'State',
                   'description': 'The state',
                   'type': 'string'}},
                 'required': ['street', 'city', 'state']}]}},
             'required': ['name', 'address']}]}},
         'required': ['name', 'email', 'address']}},
       'required': ['user'],
       'definitions': {}}}},
    {'type': 'object',
     'description': 'Retrieves the user ID from the username for Instagram API v7.\n\nArgs:\n    username (str): The username of the user.\n\nReturns:\n    Optional[User]: The user object with the retrieved user ID, or None if the user is not found.',
     'properties': {'name': {'const': 'get_user_id_from_username_for_instagram_v7'},
      'arguments': {'type': 'object',
       'properties': {'username': {'title': 'Username', 'type': 'string'}},
       'required': ['username']}}}]}},
 'required': ['observation', 'thought', 'criticism']}
    print(get_complexity_obj(schema,use_original_key=True,raise_warning=True))