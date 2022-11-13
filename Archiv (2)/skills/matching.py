from neomodel import db

from skills.models.skills import Skill

QUERY_BY_COURSE = '''
    MATCH
        (course:Course)-[rel:TEACHES]->(skill:Skill)
    WHERE
        course.uid=$course_uid
'''

QUERY_BY_OCCUPATION = '''
    MATCH
        (occ:OntologyOccupation)<-[rel:RELEVANT_FOR]-(skill:Skill)
    WHERE
        occ.uid=$occupation_uid
'''

QUERY_BY_PERSONALITY_TYPES = '''
    MATCH
        (pt:PersonalityType)<-[rel:RELEVANT_FOR]-(skill:Skill)
    WHERE
        pt.code IN $personality_type_codes
'''

# important to order by skill.uid to ensure pagination works reliably
QUERY_SIMILAR_SKILLS = '''
    MATCH
        (skill:Skill)-[rel1:RELEVANT_FOR]->(job:OntologyOccupation),
        (similar:Skill)-[rel2:RELEVANT_FOR]->(job)
    WHERE
        skill.uid IN $skills 
        AND similar.type IN $types 
    WITH
        DISTINCT similar as skill,
        AVG(rel1.priority)*AVG(rel2.priority)*count(job) as relevance
    ORDER BY relevance DESC, similar.uid
'''

# these query fragments are used to add even/odd row numbers to the query.
# this is useful to alternate between two results lists
ADD_EVEN_ROW_NUMBERS = '''
    WITH COLLECT(skill) as skill
    WITH REDUCE(arr=[], i IN RANGE(0,SIZE(skill)-1) | arr+[[i*2]+skill[i]]) AS skillsWithRowNumber
    UNWIND skillsWithRowNumber as skillWithRowNumber
    RETURN skillWithRowNumber[0] AS rowNumber, skillWithRowNumber[1] AS skill
'''
ADD_ODD_ROW_NUMBERS = '''
    WITH COLLECT(skill) as skills
    WITH REDUCE(arr=[], i IN RANGE(0,SIZE(skills)-1) | arr+[[1+i*2]+skills[i]]) AS skillsWithRowNumber
    UNWIND skillsWithRowNumber as skillWithRowNumber
    RETURN skillWithRowNumber[0] AS rowNumber, skillWithRowNumber[1] AS skill
'''


CV_SUGGEST_QUERY = '''
    CALL {
        MATCH
            (occ:OntologyOccupation)<-[rel:RELEVANT_FOR]-(skill:Skill)
        WHERE
            occ.uid IN $occupation_uids
        RETURN rel.priority as relevance, skill
        
        UNION ALL
        
        MATCH
            (course:Course)-[:IS]->(subject:Subject)
        WHERE
            subject.uid IN $subject_uids
        MATCH
            (course)-[rel:TEACHES]->(skill:Skill)
        RETURN rel.priority as relevance, skill
    }
    WITH DISTINCT skill, max(relevance) as relevance
    WHERE NOT skill.uid in $skills
    WITH skill, relevance
    ORDER BY relevance DESC, skill.uid
'''


def suggest_skills(occupations, subjects, skills, types, exclude=[],  limit=10):

    occupations = [occ['uid'] for occ in occupations]
    subjects = [edu['uid'] for edu in subjects]
        
    params = {
        'types': types,
        'skills': [skill['uid'] for skill in skills],
        'exclude': [skill['uid'] for skill in exclude],
        'occupation_uids': occupations,
        'subject_uids': subjects
    }

    if len(skills) >= 3:

        # limits on both queries to improve performance
        query = f'''
            CALL {{
                {CV_SUGGEST_QUERY}
                LIMIT {limit*4}
                {ADD_ODD_ROW_NUMBERS}
            UNION
                {QUERY_SIMILAR_SKILLS}
                LIMIT {limit*4}
                {ADD_EVEN_ROW_NUMBERS}
            }}
            WITH skill, rowNumber
            WHERE NOT skill.uid IN $skills AND skill.type IN $types
            AND NOT skill.uid IN $exclude
            WITH skill, rowNumber
            ORDER BY rowNumber
            RETURN DISTINCT skill
        '''
    else:
        query = f'''
            {CV_SUGGEST_QUERY}
            WHERE skill.type IN $types
            AND NOT skill.uid in $exclude
            RETURN DISTINCT skill
        '''

    query += f'LIMIT {limit}'

    results, meta = db.cypher_query(
        query,
        params
    )

    return [Skill.inflate(row[0]) for row in results]


def preselect_social_skills(personality_types, limit):
    assert personality_types, "Personality types missing for searching"
    params = {
        'limit': limit,
        'type': ['social'],
        'personality_type_codes': personality_types
    }

    query = QUERY_BY_PERSONALITY_TYPES
    
    query+='''
        AND skill.type IN $type
        WITH
            DISTINCT skill,
            sum(rel.priority) as priority
        RETURN skill
        ORDER BY priority DESC, skill.uid
        LIMIT $limit
    '''
    results, meta = db.cypher_query(
            query,
            params
        )

    return [Skill.inflate(row[0]) for row in results]


def preselect_skills(occupations, subjects):

    def run_query(query):
        return db.cypher_query(
            query,
            {
                'occupation_uids': occupations,
                'subject_uids': subjects,
                'skills': []
            }
        )[0]

    results = run_query(f'''    
        {CV_SUGGEST_QUERY}
        WHERE relevance >= 7 AND skill.type IN ['activity', 'knowledge']
        RETURN skill
    ''')

    # if there are less than 15 high-relevance skills, query again and just output the 15 most relevant ones
    if len(results) < 15:
        results = run_query(f'''    
            {CV_SUGGEST_QUERY}
            WHERE skill.type IN ['activity', 'knowledge']
            RETURN skill
            LIMIT 15
        ''')

    return [Skill.inflate(row[0]) for row in results]

def find_skills_for_course(course, type, limit=20):

    query = f'''
            MATCH
                (course:Course)-[rel:TEACHES]->(skill:Skill)
            WHERE
                course.uid=$course AND skill.user_skill=False
                {'AND skill.type=$type' if type else ''}
            WITH
                DISTINCT skill,
                avg(rel.priority) as priority
            RETURN
                skill
            ORDER BY priority DESC
            LIMIT $limit
    '''

    results, meta = db.cypher_query(
        query,
        params={
            'limit': limit,
            'type': type,
            'course': course.uid
    })

    return [Skill.inflate(row[0]) for row in results]


def find_skills_for_occupation(occupation, type, limit=20):

    query = f'''
            MATCH
                (occupation:OntologyOccupation)<-[rel:RELEVANT_FOR]-(skill:Skill)
            WHERE
                occupation.uid=$occupation
                {'AND skill.type=$type' if type else ''}
            RETURN
                skill
            ORDER BY skill.priority DESC
            LIMIT $limit
    '''

    results, meta = db.cypher_query(
        query,
        params={
            'limit': limit,
            'type': type,
            'occupation': occupation.uid
    })

    return [Skill.inflate(row[0]) for row in results]
