# Standard library imports
import json

# Local imports
from uplink.converters import interfaces, register


class Cast(interfaces.Converter):
    def __init__(self, caster, converter):
        self._cast = caster
        self._converter = converter

    def convert(self, value):
        if callable(self._cast):
            value = self._cast(value)
        return self._converter(value)


class RequestBodyConverter(interfaces.Converter):
    def convert(self, value):
        if isinstance(value, str):
            return value
        else:
            return json.loads(
                json.dumps(value, default=lambda obj: obj.__dict__)
            )


class StringConverter(interfaces.Converter):
    def convert(self, value):
        return str(value)


@register.register_converter_factory
class StandardConverter(interfaces.ConverterFactory):
    """
    The default converter, this class seeks to provide sane alternatives
    for (de)serialization when all else fails -- e.g., no other
    converters could handle a particular type.
    """

    def make_response_body_converter(self, type_, *args, **kwargs):
        if callable(type_):
            return type_

    def make_request_body_converter(self, type_, *args, **kwargs):
        return Cast(type_, RequestBodyConverter())  # pragma: no cover

    def make_string_converter(self, type_, *args, **kwargs):
        return Cast(type_, StringConverter())  # pragma: no cover
