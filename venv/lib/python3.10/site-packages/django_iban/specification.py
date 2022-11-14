from collections import namedtuple

from django_iban.utils import clean_iban

IBANPartSpecification = namedtuple('IBANPartSpecification', ["length", "data_type"])


class IBANSpecification(object):
    MASK_DATATYPE_MAP = {
        'a':'a',
        'n':'9',
        'c':'w',
    }

    REGEX_DATATYPE_MAP = {
        'a': '[A-Z]'   ,
        'n': '[0-9]'   ,
        'c': '[A-Z0-9]',
    }

    def __init__(self, country_name, country_code, bank_format, account_format):
        self.country_name          = country_name
        self.country_code          = country_code
        self.bank_specification    = self.decode_format(bank_format   )
        self.account_specification = self.decode_format(account_format)

    @property
    def bank_field_length(self):
        return sum((_.length for _ in self.bank_specification))

    @property
    def account_field_length(self):
        return sum((_.length for _ in self.account_specification))

    def field_mask(self, specification):
        return " ".join([
            self.MASK_DATATYPE_MAP[part.data_type] * part.length
            for part in specification if part.length > 0])

    def validation_regex(self, specification):
        return "".join([
            "%s{%s}" % (self.REGEX_DATATYPE_MAP[part.data_type], part.length)
            for part in specification if part.length > 0])

    @property
    def bank_regex(self):
        return self.validation_regex(self.bank_specification)

    @property
    def account_regex(self):
        return self.validation_regex(self.account_specification)

    @property
    def iban_regex(self):
        return "[A-Z]{2}[0-9]{2}" + self.bank_regex + self.account_regex

    @property
    def bank_field_mask(self):
        return self.field_mask(self.bank_specification)

    @property
    def account_field_mask(self):
        return self.field_mask(self.account_specification)

    @property
    def total_length(self):
        return 4 + self.bank_field_length + self.account_field_length

    def decode_format(self, data_format):
        return [
            IBANPartSpecification(
                length    = int(part[:-1]) if part[-1] in ("n", "a") else int(part),
                data_type = part[-1]       if part[-1] in ("n", "a") else "c")
            for part in filter(bool, data_format.split())]

    @staticmethod
    def checksum(value):
        value = clean_iban(value)
        value = value[4:] + value[:2] + '00'
        value_digits = ''
        for x in value:
            if '0' <= x <= '9':
                value_digits += x
            elif 'A' <= x <= 'Z':
                value_digits += str(ord(x) - 55)
            else:
                raise Exception('{} is not a valid character for IBAN.'.format(x))
        return '%02d' % (98 - int(value_digits) % 97)


IBAN_SPECIFICATION_CONFIG = {
    "AD": IBANSpecification("Andorra"               , "AD", "0  4n 4n", "0  12   0 "),
    "AL": IBANSpecification("Albania"               , "AL", "0  8n 0 ", "0  16   0 "),
    "AT": IBANSpecification("Austria"               , "AT", "0  5n 0 ", "0  11n  0 "),
    "BA": IBANSpecification("Bosnia and Herzegovina", "BA", "0  3n 3n", "0   8n  2n"),
    "BE": IBANSpecification("Belgium"               , "BE", "0  3n 0 ", "0   7n  2n"),
    "BG": IBANSpecification("Bulgaria"              , "BG", "0  4a 4n", "2n  8   0 "),
    "CH": IBANSpecification("Switzerland"           , "CH", "0  5n 0 ", "0  12   0 "),
    "CY": IBANSpecification("Cyprus"                , "CY", "0  3n 5n", "0  16   0 "),
    "CZ": IBANSpecification("Czech Republic"        , "CZ", "0  4n 0 ", "0  16n  0 "),
    "DE": IBANSpecification("Germany"               , "DE", "0  8n 0 ", "0  10n  0 "),
    "DK": IBANSpecification("Denmark"               , "DK", "0  4n 0 ", "0   9n  1n"),
    "EE": IBANSpecification("Estonia"               , "EE", "0  2n 0 ", "2n 11n  1n"),
    "ES": IBANSpecification("Spain"                 , "ES", "0  4n 4n", "2n 10n  0 "),
    "FI": IBANSpecification("Finland"               , "FI", "0  6n 0 ", "0   7n  1n"),
    "FO": IBANSpecification("Faroe Islands"         , "FO", "0  4n 0 ", "0   9n  1n"),
    "FR": IBANSpecification("France"                , "FR", "0  5n 5n", "0  11   2n"),
    "GB": IBANSpecification("United Kingdom"        , "GB", "0  4a 6n", "0   8n  0 "),
    "GE": IBANSpecification("Georgia"               , "GE", "0  2a 0 ", "0  16n  0 "),
    "GI": IBANSpecification("Gibraltar"             , "GI", "0  4a 0 ", "0  15   0 "),
    "GL": IBANSpecification("Greenland"             , "GL", "0  4n 0 ", "0   9n  1n"),
    "GR": IBANSpecification("Greece"                , "GR", "0  3n 4n", "0  16   0 "),
    "HR": IBANSpecification("Croatia"               , "HR", "0  7n 0 ", "0  10n  0 "),
    "HU": IBANSpecification("Hungary"               , "HU", "0  3n 4n", "1n 15n  1n"),
    "IE": IBANSpecification("Ireland"               , "IE", "0  4a 6n", "0   8n  0 "),
    "IL": IBANSpecification("Israel"                , "IL", "0  3n 3n", "0  13n  0 "),
    "IS": IBANSpecification("Iceland"               , "IS", "0  4n 0 ", "2n 16n  0 "),
    "IT": IBANSpecification("Italy"                 , "IT", "1a 5n 5n", "0  12   0 "),
    "KW": IBANSpecification("Kuwait"                , "KW", "0  4a 0 ", "0  22   0 "),
    "KZ": IBANSpecification("Kazakhstan"            , "KZ", "0  3n 0 ", "0  13   0 "),
    "LB": IBANSpecification("Lebanon"               , "LB", "0  4n 0 ", "0  20   0 "),
    "LI": IBANSpecification("Liechtenstein"         , "LI", "0  5n 0 ", "0  12   0 "),
    "LT": IBANSpecification("Lithuania"             , "LT", "0  5n 0 ", "0  11n  0 "),
    "LU": IBANSpecification("Luxembourg"            , "LU", "0  3n 0 ", "0  13   0 "),
    "LV": IBANSpecification("Latvia"                , "LV", "0  4a 0 ", "0  13   0 "),
    "MC": IBANSpecification("Monaco"                , "MC", "0  5n 5n", "0  11   2n"),
    "ME": IBANSpecification("Montenegro"            , "ME", "0  3n 0 ", "0  13n  2n"),
    "MK": IBANSpecification("Macedonia"             , "MK", "0  3n 0 ", "0  10   2n"),
    "MR": IBANSpecification("Mauritania"            , "MR", "0  5n 5n", "0  11n  2n"),
    "MT": IBANSpecification("Malta"                 , "MT", "0  4a 5n", "0  18   0 "),
    "MU": IBANSpecification("Mauritius"             , "MU", "0  4a 4n", "0  15n  3a"),
    "NL": IBANSpecification("Netherlands"           , "NL", "0  4a 0 ", "0  10n  0 "),
    "NO": IBANSpecification("Norway"                , "NO", "0  4n 0 ", "0   6n  1n"),
    "PL": IBANSpecification("Poland"                , "PL", "0  8n 0 ", "0  16n  0 "),
    "PT": IBANSpecification("Portugal"              , "PT", "0  4n 4n", "0  11n  2n"),
    "RO": IBANSpecification("Romania"               , "RO", "0  4a 0 ", "0  16   0 "),
    "RS": IBANSpecification("Serbia"                , "RS", "0  3n 0 ", "0  13n  2n"),
    "SA": IBANSpecification("Saudi Arabia"          , "SA", "0  2n 0 ", "0  18   0 "),
    "SE": IBANSpecification("Sweden"                , "SE", "0  3n 0 ", "0  16n  1n"),
    "SI": IBANSpecification("Slovenia"              , "SI", "0  5n 0 ", "0   8n  2n"),
    "SK": IBANSpecification("Slovak Republic"       , "SK", "0  4n 0 ", "0  16n  0 "),
    "SM": IBANSpecification("San Marino"            , "SM", "1a 5n 5n", "0  12   0 "),
    "TN": IBANSpecification("Tunisia"               , "TN", "0  2n 3n", "0  13n  2n"),
    "TR": IBANSpecification("Turkey"                , "TR", "0  5n 0 ", "1  16   0 ")}


IBAN_GROUPING   = 4
IBAN_MAX_LENGTH = 34
IBAN_MIN_LENGTH = min([_.total_length for _ in IBAN_SPECIFICATION_CONFIG.values()])
