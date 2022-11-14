from re                       import match
from django.core.exceptions   import ValidationError
from django.utils.translation import ugettext_lazy as _

from django_iban.utils         import clean_iban
from django_iban.specification import IBAN_SPECIFICATION_CONFIG


class IBANValidator(object):
    def __call__(self, value):
        if value is not None:
            value         = clean_iban(value)
            country_code  = value[:2]
            iban_checksum = value[2:4]

            # Check if the country is in the known list
            if country_code not in IBAN_SPECIFICATION_CONFIG:
                raise ValidationError(_('The country code does not correspond to any of the know iban specifications'))

            # Decoding the specific country specification
            country_data = IBAN_SPECIFICATION_CONFIG[country_code]

            # Checking if the iban matches the country specification
            if not match(country_data.iban_regex, value):
                raise ValidationError(_('The IBAN does not match the expected format for this country'))

            if country_data.checksum(value) != iban_checksum:
                raise ValidationError(_('The IBAN checksum is invalid.'))
