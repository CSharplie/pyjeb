"""PyJeb Exceptions"""

class InvalidParameterException(Exception):
    """Invalid parameter exception"""

class NotProvidedParameterException(InvalidParameterException):
    """A parameter is not provided"""

class EmptyParameterException(InvalidParameterException):
    """A parameter is not provided"""

class InvalidTypeParameterException(InvalidParameterException):
    """A parameter is not the correct type"""

class InvalidValueParameterException(InvalidParameterException):
    """A parameter value is correct"""

class CustomFunctionException(Exception):
    """Custom parameter exception"""
