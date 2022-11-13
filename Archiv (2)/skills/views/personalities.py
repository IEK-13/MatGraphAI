from rest_framework import viewsets

from graphutils.viewsets import GenericNeoViewSet
from skills.models.base import PersonalityType
from skills.serializers import PersonalityTypeSerializer


class PersonalityView(GenericNeoViewSet, viewsets.mixins.ListModelMixin):

    serializer_class = PersonalityTypeSerializer
    model = PersonalityType
