from os.path                  import join
from os.path                  import dirname
from os.path                  import abspath
from django.db                import connection
from itertools                import chain
from django.apps              import AppConfig
from django.conf              import settings
from django.db.models.signals import pre_migrate

from django_iban.fields import IBANField


class IBANFieldConfig(AppConfig):
    name         = 'django_iban'
    verbose_name = 'Django IBAN Field'

    def ready(self):
        pre_migrate.connect(self.enforce_database_constraint_callback)

    def enforce_database_constraint_callback(self, sender, **kwargs):
        database_backend = settings.DATABASES['default']['ENGINE']
        enforcing_status = any([
            iban_field.enforce_database_constraint
            for iban_field in chain.from_iterable([
                model._meta.fields for model in sender.get_models()])
            if isinstance(iban_field, IBANField)])

        if database_backend in (
            'django.db.backends.postgresql_psycopg2',
            'django.contrib.gis.db.backends.postgis'
        ) and enforcing_status:
            cursor    = connection.cursor()
            base_path = dirname(abspath(__file__))

            cursor.execute("select * from pg_available_extensions where name = 'plpythonu'")
            if cursor.rowcount == 1:
                cursor.execute(
                    """
                    SELECT p.proname FROM pg_catalog.pg_namespace n JOIN pg_catalog.pg_proc p
                    ON p.pronamespace = n.oid
                    WHERE n.nspname = 'public' AND p.proname = 'is_valid_iban';
                    """)

                if cursor.rowcount != 1:
                    with open(join(base_path, 'pg_iban_validator.sql')) as iban_type_definition:
                        cursor.execute(iban_type_definition.read())
            else:
                raise Exception('django_iban requested database enforcing but plpython extension not installed!')
