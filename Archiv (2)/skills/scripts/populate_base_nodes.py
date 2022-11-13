from skills import JobCategory, PersonalityType, Canton, CompanySize


def run():

    JobCategory.create_or_update(
        {'rdb_id': 8, 'uid': '157c4b2739a1431a84955a15a5af5632', 'label': 'Einstiegsstelle'},
        {'rdb_id': 7, 'uid': '08140e0a0df9434bbb3d45bc3644dde3', 'label': 'Saisonal'},
        {'rdb_id': 6, 'uid': '9c97594d04a64d36a7af7e4af1c8d1e0', 'label': 'Praktikum'},
        {'rdb_id': 5, 'uid': '7732cda465a948938fef38d1cd2726d8', 'label': 'Festanstellung'},
        {'rdb_id': 4, 'uid': '90a46eb03ceb4d92b287044361a63bce', 'label': 'Aushilfsjobs'},
        {'rdb_id': 3, 'uid': '5d4bf01e3624485e93b76dc4ec71c8e8', 'label': 'Trainee'},
        {'rdb_id': 2, 'uid': 'c6689b14c4da4c2888614b19875d3b18', 'label': 'PhD / Doktorat'},
        {'rdb_id': 1, 'uid': '394110bd06c549e388e3f0c3897e6c6b', 'label': 'Werkstudent / Nebenjob'}
    )

    PersonalityType.create_or_update(
        {'code': 'analyst',         'label': 'Kritisches Analysieren'},
        {'code': 'freigeist',       'label': 'Kreatives Denken'},
        {'code': 'leader',          'label': 'Entscheidungsfreudiges Führen'},
        {'code': 'netzwerker',      'label': 'Unternehmerisches Netzwerken'},
        {'code': 'planer',          'label': 'Konzeptionelles Planen'},
        {'code': 'umsetzer',        'label': 'Effizientes Umsetzen'},
        {'code': 'unterstuetzer',   'label': 'Vielseitiges Unterstützen'},
        {'code': 'verkaeufer',      'label': 'Enthusiastisches Verkaufen'}
    )

    Canton.create_or_update(
        {'code': 'ZH', 'label': 'Zürich'},
        {'code': 'BE', 'label': 'Bern'},
        {'code': 'LU', 'label': 'Luzern'},
        {'code': 'UR', 'label': 'Uri'},
        {'code': 'SZ', 'label': 'Schwyz'},
        {'code': 'OW', 'label': 'Obwalden'},
        {'code': 'NW', 'label': 'Nidwalden'},
        {'code': 'GL', 'label': 'Glarus'},
        {'code': 'ZG', 'label': 'Zug'},
        {'code': 'FR', 'label': 'Freiburg'},
        {'code': 'SO', 'label': 'Solothurn'},
        {'code': 'BS', 'label': 'Basel-Stadt'},
        {'code': 'BL', 'label': 'Basel-Landschaft'},
        {'code': 'SH', 'label': 'Schaffhausen'},
        {'code': 'AR', 'label': 'Appenzell Ausserrhoden'},
        {'code': 'AI', 'label': 'Appenzell Innerrhoden'},
        {'code': 'SG', 'label': 'St. Gallen'},
        {'code': 'GR', 'label': 'Graubünden'},
        {'code': 'AG', 'label': 'Aargau'},
        {'code': 'TG', 'label': 'Thurgau'},
        {'code': 'TI', 'label': 'Tessin'},
        {'code': 'VD', 'label': 'Waadt'},
        {'code': 'VS', 'label': 'Wallis'},
        {'code': 'NE', 'label': 'Neuenburg'},
        {'code': 'GE', 'label': 'Genf'},
        {'code': 'JU', 'label': 'Jura'}
    )

    CompanySize.create_or_update(
        {'x28_id': 57000001,'uid': '780631e5d09e43f49ab87ecb317b12f5', 'label': 'Kleinstunternehmen'},
        {'x28_id': 57000002,'uid': '31365e8efb314a2c904775a0f2cef88f', 'label': 'Kleinunternehmen'},
        {'x28_id': 57000003,'uid': 'b276217afe704a5f8b1d1a42480b42be', 'label': 'Mittelunternehmen'},
        {'x28_id': 57000004,'uid': 'f683bd6694554a12832abebad5a08061', 'label': 'Grossunternehmen'}
    )
