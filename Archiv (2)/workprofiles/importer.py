from skills.models.education import Subject, Degree
from skills.models.ontology import OntologyOccupation
from workprofiles.models import ExternalWorkProfile
from datetime import datetime
from neomodel import db

from skills.models.skills import Skill

DEGREES = [
    {
        'node': "Bachelor",
        'names': ['bachelor']
    },
    {
        'node': "Master",
        'names': ['master']
    },
    {
        'node': "Doktorat",
        'names': ['phd', 'doktorat', 'promotion']
    },
]

# date format is 2021.01
def date_linkedin_to_internal(input):
    try:
        return datetime.strptime(
            input,
            '%Y.%m' if input.find('.') != -1 else '%Y'
        ).date()
    except ValueError:
        return None


def convert_dates(item):
    item['since'] = date_linkedin_to_internal(item['since'])
    item['until'] = date_linkedin_to_internal(item['until'])
    return item

def extract_list(row, attributes):

    items = []

    for index in range(1, len(row)):

        # no more columns to process
        if list(attributes.values())[0]+'_'+str(index) not in row:
            break

        item = {}

        for key, col_name in attributes.items():
            item[key] = row[f'{col_name}_{index}'].strip()

        items.append(
            convert_dates(item)
        )

    return items


@db.read_transaction
def parse_occupations(row):

    occupations = []

    items = extract_list(row, {
        'company': 'organization',
        'title': 'organization_title',
        'since': 'organization_start',
        'until': 'organization_end',
        'description': 'organization_description'
    })

    for item in items:

        if item['title']:

            query = '''
                MATCH
                    (occ:OntologyOccupation)
                UNWIND
                    occ.alternative_labels as label
                WITH
                    occ, label, apoc.text.levenshteinSimilarity(label, $q) as distance
                ORDER BY distance DESC
                RETURN
                    occ
                LIMIT 1
            '''
            result, meta = db.cypher_query(query, {'q': item['title']})

            if result:
                occupations.append({
                    'occupation': OntologyOccupation.inflate(result[0][0]),
                    **item
                })

    return occupations


def find_school(name):

    if not name:
        return None

    query = '''
        MATCH
            (school:School)
        WITH
            school, apoc.text.levenshteinSimilarity(school.label, $q) as distance
        WHERE distance > 0.45
        RETURN school.uid
        ORDER BY distance DESC
        LIMIT 1
    '''

    result, meta = db.cypher_query(query, {'q': name})

    return result[0][0] if result else None

def find_skills(skills):

    skills = skills.split(',')

    if len(skills) == 0:
        return []

    skills = list(map(lambda skill: skill.replace(' : null', ''), skills))

    query = '''
        UNWIND $labels as search_term
        MATCH
            (skill:Skill)
        UNWIND
            skill.alternative_labels as label
        WITH
            skill,
            apoc.text.levenshteinSimilarity(label, search_term) as distance
        WHERE
            distance > 0.7
        RETURN DISTINCT skill
    '''

    result, meta = db.cypher_query(query, {'labels': skills})

    return [Skill.inflate(row[0]) for row in result]

def find_subject(name):

    if not name:
        return None

    query = '''
        MATCH
            (sub:Subject)
        WITH
            sub, apoc.text.levenshteinSimilarity(sub.label, $q) as distance
        RETURN sub
        ORDER BY distance DESC
        LIMIT 1
    '''

    result, meta = db.cypher_query(query, {'q': name})

    return Subject.inflate(result[0][0]) if result else None


def find_degree(name):
    if name:
        for degree in DEGREES:
            for name in degree['names']:
                if name.lower().find(name) != -1:
                    return degree['node'].uid
    return None


@db.read_transaction
def parse_educations(row):

    educations = []

    items = extract_list(row, {
        'school': 'education',
        'title': 'education_fos',
        'since': 'education_start',
        'until': 'education_end',
        'degree': 'education_degree'
    })

    for item in items:
        if subject := find_subject(item['title']):
            school = find_school(item.pop('school'))
            degree = find_degree(item.pop('degree'))

            educations.append({
                'subject': subject,
                'school': school,
                'degree': degree,
                **item
            })

    return educations


# used to populate node objects upon import
def populate_degrees():
    for deg in DEGREES:
        if isinstance(deg['node'], str):
            deg['node'] = Degree.nodes.get(label=deg['node'])


def import_wp_csv(reader, message_user, request):

    populate_degrees()

    total_row_number = 0
    successfully_imported_profiles = 0
    duplicate_data = 0

    for row in reader:
        total_row_number += 1

        if not row['public_id']:
            continue

        # check for duplicate
        if ExternalWorkProfile.nodes.get_or_none(import_identifier=row['public_id']):
            duplicate_data += 1
            continue

        about_me = [
            row['headline'],
            row['location_name'],
            row['summary']
        ]

        profile = ExternalWorkProfile.create({
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'import_identifier': row['public_id'],
            'about_me': '\n\n'.join(about_me),
            'imported_data': row,
            'imported_unchecked': True,
            'source': 'import',
            'profile_url': row['profile_url']
        })[0]
        successfully_imported_profiles += 1

        for item in parse_educations(row):
            subject = item.pop('subject')
            profile.educations.connect(subject, item)

        for item in parse_occupations(row):
            occupation = item.pop('occupation')
            profile.occupations.connect(occupation, item)

        for skill in find_skills(row['skills']):
            profile.skills.connect(skill)

        profile.preselect_skills()

    message_user(request, "Total rows in CSV file: "+str(total_row_number))
    message_user(request, "Imported profiles: " + str(successfully_imported_profiles))
    message_user(request, "Duplicate data ignored: "+str(duplicate_data))