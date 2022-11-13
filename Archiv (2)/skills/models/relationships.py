from neomodel import StructuredRel, IntegerProperty, BooleanProperty


class RelevantForRel(StructuredRel):
    priority = IntegerProperty(
        required=False,
        default=1
    )


class RequiresSkillRel(StructuredRel):
    relevance = IntegerProperty(default=1)  # 1..4 (relevant..essential)


class PossessesSkillRel(StructuredRel):
    level = IntegerProperty(default=1) # 1..4 (beginner..expert)
    likes = BooleanProperty(default=False)
