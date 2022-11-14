######################
django-iban-field
######################

Django iban field with validators and optional postgresql in base constraint checking. This is
expected to work with django 1.8 and later.

Installation
=============

Install ``django-iban-field`` like you would install any other pypi package::

    pip install django-iban-field


Configuration and usage
========================

* add ``django_iban`` to the list of ``INSTALLED_APPS`` in your ``settings.py``
* use in ``models.py``::

    from django_iban.fields import IBANField

    ...

    class MyModel(models.Model):
        iban = IBANField(enforce_database_constraint=True, unique=True)

The ``enable_databse_constraint`` option will add a function named is_valid_iban to your database and
use it the enforce the database type checking. This option will have an effect only if you are using
the postgreql backend and have the ``plpython`` extension enabled on your database.


Utilities
=========

Other than the django field, you will find a generator class to use if you want to generate valid
IBAN values::

    from django_iban.generator import IBANGenerator

    ....
    generator = IBANGenerator()
    # A complete random IBAN
    valid_iban = generator.generate()
    # But you can specify the country
    valid_iban = generator.generate(country_code='DE')
    # Or the bank and account
    valid_iban = generator.generate(country_code='DE', bank=XXXX, account=XXXX)

You cannot of course just pass the bank and the account without the country, and if you pass one 
or both of these values will then check for their validity, compute the checksum and return the
valid IBAN.

You may also be intereseted in the IBANSpecification class that contains all the format specification
and the checksum facility::

    from django_iban.specification import IBANSpecification
    from django_iban.specification import IBAN_SPECIFICATION_CONFIG

    ....
    country_specification = IBAN_SPECIFICATION_CONFIG['TN']
    print(country_specification.bank_field_length)
    # 5
    print(country_specification.bank_regex)
    #[0-9]{2}[0-9]{3}
    print(country_specification.iban_regex)
    #[A-Z]{2}[0-9]{2}[0-9]{2}[0-9]{3}[0-9]{13}[0-9]{2}


Inspiration
===========

This module take it's inspiration and some of the ideas from the `django-localflavor`_
IBanField and the specification from `tom's cafe`_

Example
=======

You can find a running example of this field in this `demo django application`_, and if you are super lazy
you can just get my `vagrant bootstraper script` that will setup a full working vm using that project. You
just have to have vagrant and openssl installed (tested on Fedora but should work with any other modern linux 
or mac)::

    curl https://raw.githubusercontent.com/Chedi/DjangoVagrantBootsraper/master/bootstrap.sh | bash


.. _`demo django application`: https://github.com/Chedi/test_app
.. _`tom's cafe`: http://toms-cafe.de/iban/iban.py
.. _`django-localflavor`: http://django-localflavor.readthedocs.org/en/latest/


