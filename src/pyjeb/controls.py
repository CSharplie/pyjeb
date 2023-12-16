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
    ]

def check_validset(name, value, validset):
   if type(validset) is str or type(validset) is int:
      validset = [validset]

   if type(validset) is not list:
      raise ValueError(f"'validset' property must be a string or array")
   
   validset_str = "', '".join(validset)
   if value not in validset:
      raise ValueError(f"'{value}' is not a valid value for property '{name}'. The value must be one of these values: '{validset_str}'")
