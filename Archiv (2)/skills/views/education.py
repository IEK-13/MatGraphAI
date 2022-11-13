from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from graphutils.serializers import LabeledDjangoNodeSerializer
from graphutils.viewsets import GenericNeoViewSet
from skills.models.education import School, Course, Subject
from skills.serializers import CourseSerializer
from neomodel import db


class SchoolView(GenericNeoViewSet, viewsets.mixins.ListModelMixin):

    serializer_class = LabeledDjangoNodeSerializer
    model = School

    @action(methods=['get'], detail=True)
    def subjects(self, request, pk=None):
        with db.read_transaction:
            return Response(
                LabeledDjangoNodeSerializer(self.get_object().subjects, many=True).data
            )

    @action(methods=['get'], detail=True, url_path='degrees-for-subject/(?P<subject>[\w-]+)')
    def degrees_for_subject(self, request, pk=None, subject=None):

        with db.read_transaction:

            school = self.get_object()
            results, meta = school.cypher('''
                MATCH
                    (course:Course)-[:IS]->(subject:Subject),
                    (school:School)-[:OFFERS]->(course)
                WHERE
                    ID(school)=$self AND subject.uid=$subject
                RETURN
                    course
            ''', {'subject': subject})

            return Response(CourseSerializer(
                [Course.inflate(row[0]) for row in results],
                many=True
            ).data)


class SubjectView(GenericNeoViewSet, viewsets.mixins.ListModelMixin):

    serializer_class = LabeledDjangoNodeSerializer
    model = Subject
