import re

# control configuration for control file
def get_controls_of_controls():
    return [
         {
            "name": "name"
         },
         {
            "name": "default",
            "nocheck" : True,
         },
         {
            "name": "validset",
            "default" : None,
         },
         {
           "name": "regex",
           "default" : None,
         },   
    ]

def check_empty(name, value, default_defined, context):
   if value == None and not default_defined:
      raise ValueError(f"'{name}' property can't be empty in {context}")
   return True

def check_validset(name, value, validset):
   if type(validset) is str or type(validset) is int:
      validset = [validset]

   if type(validset) is not list:
      raise ValueError(f"'validset' property must be a string or array")
   
   validset_str = "', '".join(validset)
   if value not in validset:
      raise ValueError(f"'{value}' is not a valid value for property '{name}'. The value must be one of these values: '{validset_str}'")

   return True

def check_regex(name, value, expression):
   if not re.match(expression, value):
      raise ValueError(f"'{value}' do not match with expression '{expression}' for property '{name}'")

   return True
