from neomodel import RelationshipFrom, ZeroOrMore, RelationshipTo, One

from graphutils.models import LabeledDjangoNode, UIDDjangoNode
from skills.models.relationships import RelevantForRel


class Subject(LabeledDjangoNode):
    courses = RelationshipFrom('skills.models.education.Course', 'IS', cardinality=ZeroOrMore)


class School(LabeledDjangoNode):

    courses = RelationshipTo('skills.models.education.Course', 'OFFERS', cardinality=ZeroOrMore)

    @property
    def subjects(self):
        results, meta = self.cypher(
            '''
                MATCH
                    (sub:Subject)<-[:IS]-(:Course)<-[:OFFERS]-(school)
                WHERE ID(school)=$self
                RETURN DISTINCT sub
                ORDER BY sub.label
            '''
        )
        return [self.inflate(row[0]) for row in results]


class Degree(LabeledDjangoNode):

    courses = RelationshipFrom('skills.models.education.Course', 'IS', cardinality=ZeroOrMore)


class Course(UIDDjangoNode):

    schools = RelationshipFrom(School, 'OFFERS', cardinality=ZeroOrMore)

    subject = RelationshipTo(Subject, 'IS', cardinality=One)
    degree = RelationshipTo(Degree, 'IS', cardinality=One)

    skills = RelationshipTo('skills.models.skills.Skill', 'TEACHES', model=RelevantForRel)