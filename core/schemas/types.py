from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException
from pydantic.validators import strict_str_validator


class PhoneNumber(str):

    @classmethod
    def __get_validators__(cls):
        yield strict_str_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> str:
        v = v.strip().replace(' ', '')

        try:
            phone = parse(v)
        except NumberParseException:
            raise ValueError('invalid phone number format')
        else:
            if not is_valid_number(phone):
                raise ValueError('invalid phone number')
            return cls(format_number(phone, PhoneNumberFormat.E164))
