from django.db import models
from neomodel import RelationshipTo, BooleanProperty, IntegerProperty, \
    ZeroOrMore, DateTimeProperty, StringProperty, db, JSONProperty, DateProperty, StructuredRel

from core.models import Canton, JobCategory
from graphutils.models import UIDDjangoNode, QuotaMixin, FileUploadProperty
from jobs.relationships import ApplicationLinkClickedRel, InterestedInJobRel
from skills.models.base import PersonalityType
from skills.models.education import Subject, School, Degree
from skills.models.ontology import OntologyOccupation
from skills.models.relationships import PossessesSkillRel

from scrambl.localconfig import FRONTEND_BASE

WORKPROFILE_TYPE_CHOICES = {
    'user': 'Work Profile for User Account',
    'sm': 'Anonymous SkillMatcher result',
    'external': 'External Workprofile'
}

WORKPROFILE_SOURCE_CHOICES = {
    'import': 'Imported Profile (e.g. LinkedIn)',
    'custom': 'manually created in backend',
    'interest': 'User has expressed interest'
}


class CVMixin:

    since = DateProperty(required=False)
    until = DateProperty(required=False)

    title = StringProperty(required=True)


class CVEducationRel(CVMixin, StructuredRel):

    degree = StringProperty(required=False) # uid
    school = StringProperty(required=False) # uid


class CVOccupationRel(CVMixin, StructuredRel):

    description = StringProperty(required=False)
    company = StringProperty(required=False)


class WorkProfile(UIDDjangoNode, QuotaMixin):

    class Meta(UIDDjangoNode.Meta):
        verbose_name = 'Work Profiles'
        verbose_name_plural = 'Work Profiles'

    created = DateTimeProperty(default_now=True)

    type = StringProperty(choices=WORKPROFILE_TYPE_CHOICES, default='sm')
    user = StringProperty(required=False, index=True) # this contains the ID of the user that stored the WorkProfile

    skills = RelationshipTo('skills.models.skills.Skill', 'HAS_SKILL', model=PossessesSkillRel)
    personality_types = RelationshipTo(PersonalityType, 'IS')

    open_for_remote_work = BooleanProperty(
        default=True,
    )

    min_quota = IntegerProperty(
        default=10,
    )
    max_quota = IntegerProperty(
        default=100,
    )

    application_documents = FileUploadProperty()
    profile_url = StringProperty(default="")

    company_sizes = RelationshipTo('jobs.models.CompanySize', 'CAN_WORK_IN', cardinality=ZeroOrMore)

    cantons = RelationshipTo(Canton, 'CAN_WORK_IN', cardinality=ZeroOrMore)
    job_categories = RelationshipTo(JobCategory, 'IS_LOOKING_FOR', cardinality=ZeroOrMore)

    application_links_clicked = RelationshipTo('jobs.models.JobAdvert', 'CLICKED_ON', model=ApplicationLinkClickedRel)
    interested_in_jobs = RelationshipTo('jobs.models.JobAdvert', 'IS_INTERESTED_IN', model=InterestedInJobRel)

    occupations = RelationshipTo(OntologyOccupation, 'WORKED_AS', cardinality=ZeroOrMore, model=CVOccupationRel)
    educations = RelationshipTo(Subject, 'STUDIED', cardinality=ZeroOrMore, model=CVEducationRel)

    def has_application_documents(self):
        return bool(self.application_documents and len(self.application_documents) > 0)

    def __str__(self):
        return self.uid

    def skill_count(self):
        return len(self.skills)

    @property
    def name(self):
        if self.type == 'user':
            from users.models import ScramblUser
            return ScramblUser.objects.get(id=self.user).name()
        return self.uid

    @classmethod
    def for_user(cls, user, raise_exception=True):
        try:
            return cls.nodes.get(type='user', user=user.id.hex)
        except cls.DoesNotExist:
            if raise_exception:
                raise
            return None

    @db.write_transaction
    def preselect_skills(self):

        query = '''
            MATCH (wp:WorkProfile)
            WHERE ID(wp)=$self
            CALL {
                WITH wp
                MATCH (skill:Skill)-[rel:RELEVANT_FOR]->(occ:OntologyOccupation)<-[:WORKED_AS]-(wp)
                RETURN skill, rel.priority as relevance
                
                UNION ALL
                
                WITH wp
                MATCH (skill:Skill)<-[rel:TEACHES]-(:Course)-[:IS]->(subject:Subject)<-[:STUDIED]-(wp)
                RETURN skill, rel.priority as relevance
            } 
            WITH DISTINCT skill, SUM(relevance) as relevance, wp
            ORDER BY relevance DESC
            LIMIT 50
            MERGE (wp)-[rel:HAS_SKILL]->(skill)
            ON CREATE SET rel.level=1, rel.likes=false
        '''

        results, meta = self.cypher(query)

        query = '''
            MATCH (wp:WorkProfile)-[:IS]->(:PersonalityType)<-[rel:RELEVANT_FOR]-(skill:Skill)
            WHERE ID(wp)=$self
            WITH DISTINCT skill, wp, SUM(rel.priority) as priority
            ORDER BY priority DESC
            LIMIT 10
            MERGE (wp)-[new_rel:HAS_SKILL]->(skill)
            ON CREATE SET new_rel.level=1, new_rel.likes=false
        '''

        results, meta = self.cypher(query)

    def _strip_none(self, dict):
        for key, value in dict.copy().items():
            if value is None:
                del dict[key]
        return dict

    def get_educations(self):

        results, meta = self.cypher('''
            MATCH (wp)-[rel:STUDIED]->(sub:Subject)
            WHERE ID(wp)=$self
            RETURN sub.uid as uid, rel.title as title, rel.since as since, rel.until as until, rel.degree as degree, rel.school as school
        ''')

        return [self._strip_none({
            'uid': row[0],
            'title': row[1],
            'since': row[2],
            'until': row[3],
            'degree': Degree.nodes.get(uid=row[4]) if row[4] else None,
            'school': School.nodes.get(uid=row[5]) if row[5] else None
        }) for row in results]

    def get_occupations(self):

        results, meta = self.cypher('''
            MATCH (wp)-[rel:WORKED_AS]->(occ:OntologyOccupation)
            WHERE ID(wp)=$self
            RETURN occ.uid as uid, rel.title as title, rel.since as since, rel.until as until, rel.company as company, rel.description as description
        ''')

        return [self._strip_none({
            'uid': row[0],
            'title': row[1],
            'since': row[2],
            'until': row[3],
            'company': row[4],
            'description': row[5],
        }) for row in results]


class ExternalWorkProfile(WorkProfile):

    class Meta(WorkProfile.Meta):
        verbose_name = 'Externes Talentprofil'
        verbose_name_plural = 'Externe Talentprofile'

    type = StringProperty(choices=WORKPROFILE_TYPE_CHOICES, default='external')

    first_name = StringProperty(default="", index=True)
    last_name = StringProperty(default="", index=True)

    interests = StringProperty(required=False)
    about_me = StringProperty(required=False)

    email = StringProperty(required=False, index=True)
    phone_number = StringProperty(required=False)
    notes = StringProperty(required=False)

    # set to true when user has registered. These profiles are excluded from matching
    claimed = BooleanProperty(default=False)

    # set to True for imported profiles, that need to be checked. Unchecked profiles are excluded from matching
    imported_unchecked = BooleanProperty(default=False)

    # UID from linkedin etc; used to avoid importing duplicates
    import_identifier = StringProperty(required=False)
    imported_data = JSONProperty(required=False)

    source = StringProperty(choices=WORKPROFILE_SOURCE_CHOICES, default='custom')

    @property
    def name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.email:
            return self.email
        else:
            return super().name

    @property
    def claim_link(self):
        return f'{FRONTEND_BASE}skills/offer?puid={self.uid}'

    def __str__(self):
        return self.name
