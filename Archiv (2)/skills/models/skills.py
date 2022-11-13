from neomodel import StringProperty, BooleanProperty, RelationshipFrom, RelationshipTo, ZeroOrOne

from graphutils.models import LabeledDjangoNode, AlternativeLabelMixin
from .ontology import OntologyTopic, OntologyOccupation, OntologyPredicate
from .relationships import RelevantForRel


class BaseSkill(LabeledDjangoNode):

    broader = RelationshipFrom('BaseSkill', 'BROADER_THAN')
    narrower = RelationshipTo('BaseSkill', 'BROADER_THAN')

    # returns the first parent if available
    # this is only meant to be a helper function for the admin-interface (ESCO-links)
    @property
    def single_parent(self):
        return self.broader.single()
    @single_parent.setter
    def single_parent(self, parent):
        if old_parent:=self.single_parent:
            self.broader.disconnect(old_parent)
        if parent:
            self.broader.connect(parent)

SKILL_TYPE_LANGUAGE = 'language'
SKILL_TYPE_KNOWLEDGE = 'knowledge'
SKILL_TYPE_ACTIVITY = 'activity'
SKILL_TYPE_SOCIAL = 'social'

SKILL_TYPE_CHOICES = {
    SKILL_TYPE_SOCIAL: 'Social Skill',
    SKILL_TYPE_KNOWLEDGE: "Knowledge Skill",
    SKILL_TYPE_ACTIVITY: 'Work Activity',
    SKILL_TYPE_LANGUAGE: 'Language Skill'
}

class Skill(BaseSkill, AlternativeLabelMixin):

    class Meta:
        app_label = 'skills'

    type = StringProperty(
        required=False,
        choices=SKILL_TYPE_CHOICES,
        index=True
    )

    user_skill = BooleanProperty(default=False)
    disabled = BooleanProperty(default=False) # disabled skills will not be exported from skill-backend

    topics = RelationshipTo(OntologyTopic, 'HAS_TOPIC')
    topic_occupations = RelationshipTo(OntologyOccupation, 'HAS_TOPIC')

    predicate = RelationshipTo(OntologyPredicate, 'HAS_PREDICATE', cardinality=ZeroOrOne)

    occupations = RelationshipTo('OntologyOccupation', 'RELEVANT_FOR', model=RelevantForRel)

    personality_types = RelationshipTo('skills.models.base.PersonalityType', 'RELEVANT_FOR', model=RelevantForRel)

    courses = skills = RelationshipFrom('skills.models.education.Course', 'TEACHES', model=RelevantForRel)

    # temporary property for imported esco-skills
    esco_concept_url = StringProperty(
        required=False,
        index=True
    )

    # returns the first topic if available
    # this is only meant to be a helper function for the admin-interface (ESCO-links)
    @property
    def single_topic(self):
        return self.topics.single()

    def __str__(self):

        if self.label:
            return self.label

        if topic := self.topics.single():
            label = topic.label
        else:
            label = "<unknown topic>"

        if pred := self.predicate.single():
            label += " "+pred.label

        return str(label)


class ESCOSkill(BaseSkill):

    class Meta:
        app_label = 'skills'

    concept_url = StringProperty(
        required=True,
        unique_index=True
    )

    code = StringProperty(
        required=False,
        unique=True
    )

    @property
    def full_label(self):
        if self.code:
            return str(self.code) + ' '+str(self.label)
        return str(self.label)