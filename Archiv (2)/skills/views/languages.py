from rest_framework import viewsets

from skills.models.skills import Skill, SKILL_TYPE_LANGUAGE
from skills.serializers import SkillSerializer


class LanguageSkillView(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):

    serializer_class = SkillSerializer

    def get_queryset(self):
        return Skill.nodes.filter(type=SKILL_TYPE_LANGUAGE).order_by('label')