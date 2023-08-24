from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _



@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^\+?1?\d{9,11}$'
    message = _(
        "Phone number must be in the format: '0999999999'. Up to 11 digits allowed."
    )
    flags = 0
