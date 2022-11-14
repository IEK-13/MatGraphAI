from django.db.models         import CharField
from django.utils.translation import ugettext_lazy as _

from django_iban.utils         import clean_iban
from django_iban.forms         import IBANFormField
from django_iban.validators    import IBANValidator
from django_iban.specification import IBAN_MAX_LENGTH


class IBANField(CharField):
    description = _('International Bank Account Number')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', IBAN_MAX_LENGTH)
        self.enforce_database_constraint = kwargs.pop('enforce_database_constraint', False)

        if not isinstance(self.enforce_database_constraint, bool):
            raise TypeError('enforce_db_constraint can only accept True or False value')

        CharField.__init__(self, *args, **kwargs)
        self.validators.append(IBANValidator())

    def deconstruct(self):
        name, path, args, kwargs = CharField.deconstruct(self)
        kwargs['enforce_database_constraint'] = self.enforce_database_constraint
        return name, path, args, kwargs

    def to_python(self, value):
        value = CharField.to_python(self, value)
        if value is not None:
            return clean_iban(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': IBANFormField}
        defaults.update(kwargs)
        return CharField.formfield(self, **defaults)

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] in (
            'django.db.backends.postgresql_psycopg2',
            'django.contrib.gis.db.backends.postgis'
        ) and self.enforce_database_constraint:
            return 'iban'
        else:
            return CharField.db_type(self, connection)
