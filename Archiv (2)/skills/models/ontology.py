from neomodel import IntegerProperty, RelationshipFrom, StringProperty, RelationshipTo, ZeroOrMore

from graphutils.models import UIDDjangoNode, AlternativeLabelMixin
from .relationships import RelevantForRel


class OntologyElement(UIDDjangoNode):

    class Meta:
        app_label = 'skills'

    ontology_id = IntegerProperty(
        required=True,
        index=True,
    )

    label = StringProperty(
        required=True
    )


class OntologyTopic(OntologyElement):

    skills = RelationshipFrom('skills.models.skills.Skill', 'HAS_TOPIC')


class OntologyPredicate(OntologyElement):

    skills = RelationshipFrom('skills.models.skills.Skill', 'HAS_PREDICATE')


class OntologyOccupation(OntologyElement, AlternativeLabelMixin):

    skills = RelationshipFrom('skills.models.skills.Skill', 'RELEVANT_FOR', model=RelevantForRel)
    clusters = RelationshipTo('skills.models.ontology.JobCluster', 'PART_OF')

class JobCluster(OntologyElement):

    occupations = RelationshipFrom('skills.models.ontology.OntologyOccupation', 'PART_OF', ZeroOrMore)


class Industry(OntologyElement):

    companies = RelationshipFrom('skills.models.jobs.Company', 'PART_OF', ZeroOrMore)
