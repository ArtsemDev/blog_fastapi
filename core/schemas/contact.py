from pydantic import BaseModel, Field, EmailStr, ValidationError
from fastapi import Form

from .types import PhoneNumber


class ContactForm(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    phone: PhoneNumber
    message: str

    @classmethod
    def as_form(
            cls,
            name: str = Form(),
            email: str = Form(),
            phone: str = Form(),
            message: str = Form(),
    ):
        try:
            return cls(name=name, email=email, phone=phone, message=message)
        except ValidationError as e:
            errors = e.errors()
            return '\n'.join(error['msg'].title() for error in errors)
