from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from neomodel import db
from rest_framework.status import HTTP_400_BAD_REQUEST

from graphutils.helpers import validate_param
from graphutils.viewsets import GenericNeoViewSet
from skills.matching import preselect_skills, preselect_social_skills
from skills.models.ontology import OntologyOccupation
from skills.models.skills import Skill
from skills.serializers import OntologyOccupationAutocompleteSerializer, SkillSerializer


AUTOCOMPLETE_LIMIT = 40


class SkillView(GenericNeoViewSet, viewsets.mixins.CreateModelMixin):

    serializer_class = SkillSerializer
    model = Skill
    queryset = Skill.nodes

    def create(self, request, *args, **kwargs):

        try:
            existing_skill = self.queryset.get_or_none(label=request.data['label'], user_skill=True)

            if existing_skill is None:
                existing_skill=self.queryset.get_or_none(uid=request.data['uid'])
                
        except KeyError:
            existing_skill = None
        
        if existing_skill is not None:
            return Response(SkillSerializer(existing_skill).data)
        else:
            return super().create(request, *args, **kwargs)
        
    @action(methods=['get'], detail=False, url_path='suggest/preselect/social')
    def preselect_social(self, request):
        personality_types = validate_param(request, 'personality_types', list=True)
        limit = validate_param(request, 'limit', type=int, default=10)
        
        with db.read_transaction:
            try:
                skills_result = preselect_social_skills(personality_types, limit)
            except AssertionError as error:
                return Response(error, status=HTTP_400_BAD_REQUEST)

        return Response(SkillSerializer(skills_result, many=True).data)

    @action(methods=['get'], detail=False, url_path='suggest/preselect')
    def preselect(self, request):
        occupations = validate_param(request, 'occupation', type='uuid', required=False, list=True, uuidAsHexStr=True)
        subjects = validate_param(request, 'subject', type='uuid', required=False, list=True, uuidAsHexStr=True)

        if not len(occupations) and not len(subjects):
            return Response(status=HTTP_400_BAD_REQUEST)

        with db.read_transaction:
            skills_result = preselect_skills(occupations, subjects)

        return Response(SkillSerializer(skills_result, many=True).data)


    @action(methods=['get'], detail=False, url_path='autocomplete/(?P<query>.+)')
    def autocomplete(self, request, query):

        with db.read_transaction:

            cypher_query = '''
                MATCH
                    (skill:Skill)
                WHERE
                    toLower(skill.label) CONTAINS toLower($q) AND NOT (skill.user_skill=true)
                RETURN
                    skill,
                    apoc.text.distance(skill.label, $q) as distance
                ORDER BY
                    distance ASC,
                    skill.label
                LIMIT
                    $limit
            '''

            results, meta = db.cypher_query(cypher_query, {'q': query, 'limit': AUTOCOMPLETE_LIMIT})

            return Response(
                SkillSerializer(
                    [Skill.inflate(row[0]) for row in results],
                    many=True
                ).data
            )

    @action(methods=['get'], detail=False, url_path='occupations/autocomplete/(?P<query>.+)')
    def autocomplete_occupations(self, request, query):

        with db.read_transaction:
            return Response(
                OntologyOccupationAutocompleteSerializer(
                    OntologyOccupation.nodes.filter(label__icontains=query).order_by('label')[:AUTOCOMPLETE_LIMIT],
                    many=True
                ).data
            )
