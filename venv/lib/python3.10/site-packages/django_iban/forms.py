from django.forms import CharField

from django_iban.utils         import clean_iban
from django_iban.validators    import IBANValidator
from django_iban.specification import IBAN_GROUPING
from django_iban.specification import IBAN_MAX_LENGTH
from django_iban.specification import IBAN_MIN_LENGTH


class IBANFormField(CharField):
    def __init__(self, grouping=IBAN_GROUPING, *args, **kwargs):
        kwargs.setdefault('max_length', IBAN_MAX_LENGTH)
        kwargs.setdefault('min_length', IBAN_MIN_LENGTH)

        self.grouping           = grouping
        self.default_validators = [IBANValidator()]
        CharField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        value = CharField.to_python(self, value)
        if value is not None:
            return clean_iban(value)

    def prepare_value(self, value):
        if value is not None:
            value = clean_iban(value)
            return ' '.join(
                value[i:i + self.grouping]
                for i in range(0, len(value), self.grouping))
