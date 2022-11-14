def clean_iban(value):
    return value.upper().replace(' ', '').replace('-', '')
