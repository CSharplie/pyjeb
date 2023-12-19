import re

# control configuration for control file
def get_controls_of_controls():
    return [
         {
            "name": "name",
            "type": "string"
         },
         {
            "name": "default",
            "type": "string",
            "nocheck" : True,
         },
         {
            "name": "validset",
            "type": "list",
            "default" : None,
         },
         {
           "name": "regex",
           "type": "string",
           "default" : None,
         },
         {
            "name": "type",
            "default" : "string",
            "validset" : ["string", "integer", "decimal", "boolean", "list", "dict"]
         },
    ]

def check_empty(value, default_defined):
   return not((value == None or str(value) == "")and not default_defined)

def check_validset(value, validset):
   return value in validset

def check_regex(name, value, expression):
   return re.match(expression, value) is not None

def check_type(value, value_type):
   match value_type.lower():
      case "integer":
         return type(value) is int or re.match(r"^-{0,1} *[\d]+$", str(value)) is not None
      case "decimal":
         return type(value) is float or re.match(r"^-{0,1} *[\d]+(([,.])[\d]+){0,1}$", str(value)) is not None
      case "boolean":
         return type(value) is bool or str(value).lower() in ["true", "false"]
      case "list":
         return type(value) is list
      case "dict":
         return type(value) is dict
      case "string":
         return type(value) is not dict and type(value) is not list
   return False

def cast_to_type(value, value_type):
   match value_type.lower():
      case "integer":
         return int(str(value).replace(" ", ""))
      case "decimal":
         return float(str(value).replace(",", ".").replace(" ", ""))
      case "boolean":
         return str(value).lower() == "true"
      case "list":
         return value
      case "dict":
         return value
      case "string":
         return value
   return None