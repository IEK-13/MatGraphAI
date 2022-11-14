CREATE EXTENSION IF NOT EXISTS plpythonu;

CREATE OR REPLACE FUNCTION is_valid_iban(iban text) RETURNS boolean AS
$$
    from re          import match
    from collections import namedtuple

    IBANPartSpecification = namedtuple('IBANPartSpecification', ["length", "data_type"])

    IBAN_SPECIFICATION = {
        "AD": ("0  4n 4n", "0  12   0 "),
        "AL": ("0  8n 0 ", "0  16   0 "),
        "AT": ("0  5n 0 ", "0  11n  0 "),
        "BA": ("0  3n 3n", "0   8n  2n"),
        "BE": ("0  3n 0 ", "0   7n  2n"),
        "BG": ("0  4a 4n", "2n  8   0 "),
        "CH": ("0  5n 0 ", "0  12   0 "),
        "CY": ("0  3n 5n", "0  16   0 "),
        "CZ": ("0  4n 0 ", "0  16n  0 "),
        "DE": ("0  8n 0 ", "0  10n  0 "),
        "DK": ("0  4n 0 ", "0   9n  1n"),
        "EE": ("0  2n 0 ", "2n 11n  1n"),
        "ES": ("0  4n 4n", "2n 10n  0 "),
        "FI": ("0  6n 0 ", "0   7n  1n"),
        "FO": ("0  4n 0 ", "0   9n  1n"),
        "FR": ("0  5n 5n", "0  11   2n"),
        "GB": ("0  4a 6n", "0   8n  0 "),
        "GE": ("0  2a 0 ", "0  16n  0 "),
        "GI": ("0  4a 0 ", "0  15   0 "),
        "GL": ("0  4n 0 ", "0   9n  1n"),
        "GR": ("0  3n 4n", "0  16   0 "),
        "HR": ("0  7n 0 ", "0  10n  0 "),
        "HU": ("0  3n 4n", "1n 15n  1n"),
        "IE": ("0  4a 6n", "0   8n  0 "),
        "IL": ("0  3n 3n", "0  13n  0 "),
        "IS": ("0  4n 0 ", "2n 16n  0 "),
        "IT": ("1a 5n 5n", "0  12   0 "),
        "KW": ("0  4a 0 ", "0  22   0 "),
        "KZ": ("0  3n 0 ", "0  13   0 "),
        "LB": ("0  4n 0 ", "0  20   0 "),
        "LI": ("0  5n 0 ", "0  12   0 "),
        "LT": ("0  5n 0 ", "0  11n  0 "),
        "LU": ("0  3n 0 ", "0  13   0 "),
        "LV": ("0  4a 0 ", "0  13   0 "),
        "MC": ("0  5n 5n", "0  11   2n"),
        "ME": ("0  3n 0 ", "0  13n  2n"),
        "MK": ("0  3n 0 ", "0  10   2n"),
        "MR": ("0  5n 5n", "0  11n  2n"),
        "MT": ("0  4a 5n", "0  18   0 "),
        "MU": ("0  4a 4n", "0  15n  3a"),
        "NL": ("0  4a 0 ", "0  10n  0 "),
        "NO": ("0  4n 0 ", "0   6n  1n"),
        "PL": ("0  8n 0 ", "0  16n  0 "),
        "PT": ("0  4n 4n", "0  11n  2n"),
        "RO": ("0  4a 0 ", "0  16   0 "),
        "RS": ("0  3n 0 ", "0  13n  2n"),
        "SA": ("0  2n 0 ", "0  18   0 "),
        "SE": ("0  3n 0 ", "0  16n  1n"),
        "SI": ("0  5n 0 ", "0   8n  2n"),
        "SK": ("0  4n 0 ", "0  16n  0 "),
        "SM": ("1a 5n 5n", "0  12   0 "),
        "TN": ("0  2n 3n", "0  13n  2n"),
        "TR": ("0  5n 0 ", "1  16   0 ")}

    validation_mapper = {
        'a': '[A-Z]'   ,
        'n': '[0-9]'   ,
        'c': '[A-Z0-9]',
    }

    def field_length(specification):
        return sum((_.length for _ in specification))

    def decode_format(data_format):
        return [IBANPartSpecification(
                length    = int(part[:-1]) if part[-1] in ("n", "a") else int(part),
                data_type = part[-1]       if part[-1] in ("n", "a") else "c")
            for part in filter(bool, data_format.split())]

    def validation_regex(specification):
        return "".join([
            "%s{%s}" % (validation_mapper[part.data_type], part.length)
            for part in specification if part.length > 0])

    value        = iban.upper()
    country_code = value[:2]

    # Check if the country is in the known list
    if country_code not in IBAN_SPECIFICATION:
        return False

    # Decoding the specific country specification
    country_data          = IBAN_SPECIFICATION[country_code]
    bank_specification    = decode_format(country_data[0])
    account_specification = decode_format(country_data[1])

    # Building the validation regex
    bank_regex      = validation_regex(bank_specification   )
    account_regex   = validation_regex(account_specification)
    iban_full_regex = "[A-Z]{2}[0-9]{2}" + bank_regex + account_regex

    # Checking if the iban matches the country specification
    if not match(iban_full_regex, iban):
        return False

    # Computing the checksum
    value = value[4:] + value[:2] + '00'
    value_digits = ''
    for x in value:
        if '0' <= x <= '9':
            value_digits += x
        elif 'A' <= x <= 'Z':
            value_digits += str(ord(x) - 55)
        else:
            return False
    checksum = '%02d' % (98 - int(value_digits) % 97)

    # Checking if the checksum matches
    if iban[2:4] == checksum:
        return True
    return False
$$
LANGUAGE 'plpythonu' VOLATILE;

CREATE DOMAIN iban AS TEXT CHECK (is_valid_iban(VALUE) );
