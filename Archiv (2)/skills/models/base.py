from django_neomodel import DjangoNode
from neomodel import StringProperty, RelationshipFrom

from skills.models.relationships import RelevantForRel


class PersonalityType(DjangoNode):

    class Meta:
        app_label = "skills"

    code = StringProperty(
        primary_key=True
    )
    label = StringProperty(
        required=True
    )
    
    skills = RelationshipFrom('skills.models.skills.Skill', 'RELEVANT_FOR', model=RelevantForRel)
