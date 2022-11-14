from random                   import choice
from string                   import digits
from string                   import ascii_uppercase
from django.utils.translation import ugettext_lazy as _

from django_iban.specification import IBANSpecification
from django_iban.specification import IBAN_SPECIFICATION_CONFIG

mixed   = ascii_uppercase + digits
letters = ascii_uppercase


class IBANGenerator(object):
    string_randomization_map = {
        'c' : lambda length: u''.join(choice(mixed  ) for _ in range(length)),
        'n' : lambda length: u''.join(choice(digits ) for _ in range(length)),
        'a' : lambda length: u''.join(choice(letters) for _ in range(length)),
    }

    def calc_iban(self, country, bank, account):
        account  = account.zfill(country.account_field_length)
        checksum = IBANSpecification.checksum(country.country_code + "00" + bank +account)
        return country.country_code + checksum + bank + account

    def randomize_field(self, field_specification):
        return "".join([
            self.string_randomization_map[part.data_type](part.length)
            for part in field_specification])

    def generate(self, country_code=None, bank=None, account=None):
        result = {
            'bank'             : bank,
            'status'           : True,
            'account'          : account,
            'country_code'     : country_code,
            'generator_message': _('Generation successful')
        }

        if country_code is None:
            country = IBAN_SPECIFICATION_CONFIG[choice(list(IBAN_SPECIFICATION_CONFIG.keys()))]
        elif country_code in IBAN_SPECIFICATION_CONFIG.keys():
            country = IBAN_SPECIFICATION_CONFIG[country_code]
        else:
            result.update({
                'status'           : False,
                'generator_message': _('Invalid country code: {}').format (country)})
            return result

        result['bank'          ] = bank    if bank    else self.randomize_field(country.bank_specification   )
        result['account'       ] = account if account else self.randomize_field(country.account_specification)
        result['country_code'  ] = country.country_code

        try:
            result['generated_iban'] = self.calc_iban(country, result['bank'], result['account'])
        except Exception as e:
            result.update({
                'status'           : False,
                'generator_message': e.message})
        return result
