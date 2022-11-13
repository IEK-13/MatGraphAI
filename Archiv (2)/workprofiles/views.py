from django.core.exceptions import SuspiciousOperation
from neomodel import db
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from graphutils.helpers import validate_param
from graphutils.models import UploadedFilesList
from graphutils.viewsets import GenericNeoViewSet
from matching.candidates import match_candidates
from skills.matching import suggest_skills
from skills.serializers import SkillSerializer
from workprofiles.models import ExternalWorkProfile, WorkProfile
from jobs.models import JobAdvert
from jobs.serializers import JobAdvertSerializer
from .serializers import ExpressInterestWithoutExternalWorkProfileSerializer, \
    ExternalWorkProfileCreatorSerializer, ExternalWorkProfileSerializer, WorkProfileSerializer, \
    CandidateMatchSerializer, WorkProfileApplicationInfoSerializer

from users.models import ScramblUser
from scrambl.utils.Mailer import Mailer


class SkillSuggestSerializer(serializers.Serializer):

    profile = WorkProfileSerializer()
    exclude = SkillSerializer(many=True)


class WorkProfilePermission(BasePermission):

    def has_permission(self, request, view):

        if view.action in ('for_job_ad', 'for_job_ad_count', 'create', 'suggest_skills'):
            return True

        if view.action in ('retrieve', 'update', 'partial_update', 'application_info'):
            return True

        return False

    def has_object_permission(self, request, view, obj):

        if view.action in ('retrieve', 'update', 'partial_update', 'application_info'):
            return request.user.pk.hex == obj.user and obj.type == 'user'

        return False




class WorkProfileView(
    GenericNeoViewSet,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.CreateModelMixin
):

    serializer_class = WorkProfileSerializer
    permission_classes = [WorkProfilePermission]
    model = WorkProfile

    @db.write_transaction
    def get_object(self):

        # get/post is only allowed for /my
        if self.kwargs['pk'] != "my":
            raise SuspiciousOperation('you are only allowed to access your own profile')

        if not self.request.user.is_authenticated:
            raise SuspiciousOperation('not authenticated')

        return WorkProfile.nodes.get_or_none(user=self.request.user.pk.hex, type='user')

    @action(methods=['get', 'patch'], detail=True, url_path='application-info')
    def application_info(self, request, pk=None):
        if request.method == 'PATCH':

            # TODO: use serializer for validation

            profile = self.get_object()
            profile.profile_url = request.data['profile_url']
            profile.application_documents = UploadedFilesList.from_future_attachments(
                request.data['application_documents']
            )
            profile.save()

            Mailer.talent_has_updated_application_data(profile)

            return Response()

        if request.method == 'GET':
            return Response(WorkProfileApplicationInfoSerializer(self.get_object()).data)


    def perform_update(self, serializer):

        # mark external profile as claimed if uid provided
        if uid := serializer.validated_data['externalProfileSourceUID']:
            if ep := ExternalWorkProfile.nodes.get_or_none(uid=uid.hex):
                ep.claimed = True
                ep.save()

        serializer.save()

    @db.read_transaction
    def work_profile_for_job_ad(self, request, count=False):

        ser = JobAdvertSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        limit = 20
        if request.user.is_staff:
            limit = None

        result = match_candidates(
            ser.validated_data,
            count=count,
            limit=limit,
            include_skill_overlap=not count,
        )

        # include full name for logged in staff members
        if not count and request.user.is_staff:
            for res in result:
                if isinstance(res['profile'], ExternalWorkProfile):
                    res['full_name'] = res['profile'].name
                else:
                    try:
                        res['full_name'] = ScramblUser.objects.get(id=res['profile'].user).name()
                    except ScramblUser.DoesNotExist:
                        pass

        return result

    @action(methods=['post'], detail=False, url_path='for-job-ad')
    def for_job_ad(self, request):

        return Response(
            CandidateMatchSerializer(
                self.work_profile_for_job_ad(request, count=False),
                many=True
            ).data
        )

    @action(methods=['post'], detail=False, url_path='for-job-ad/count')
    def for_job_ad_count(self, request):
        return Response(
            self.work_profile_for_job_ad(request, count=True)
        )

    @action(methods=['post'], detail=False, url_path='suggest-skills')
    def suggest_skills(self, request):

        ser = SkillSuggestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        types = validate_param(request, 'type', type=str, list=True, required=True)

        with db.read_transaction:
            try:
                skills_result = suggest_skills(
                    ser.initial_data['profile']['occupations'],
                    ser.initial_data['profile']['educations'],
                    ser.initial_data['profile']['skills'],
                    types,
                    exclude=ser.initial_data['exclude'],
                    limit=10
                )
            except AssertionError:
                return Response(status=HTTP_400_BAD_REQUEST)

            return Response(SkillSerializer(skills_result, many=True).data)


class ExternalWorkProfileView(GenericNeoViewSet, viewsets.mixins.RetrieveModelMixin):

    serializer_class = ExternalWorkProfileSerializer
    model = ExternalWorkProfile
    queryset = ExternalWorkProfile.nodes

    @action(methods=['patch'], detail=True, url_path='application-info')
    def application_info(self, request, pk=None):

        # TODO: use serializer for validation

        profile = self.get_object()

        profile.first_name = request.data['first_name']
        profile.last_name = request.data['last_name']
        profile.profile_url = request.data['profile_url']
        profile.application_documents = UploadedFilesList.from_future_attachments(
            request.data['application_documents']
        )
        profile.save()

        Mailer.talent_has_updated_application_data(profile)

        return Response()

    @action(methods=['post'], detail=False, url_path='interested-without-profile')
    def interested_without_profile(self, request):
        #exception is raised only when workProfile properties are missing
        #users with direct links to job postings expressing interest
        ser = ExpressInterestWithoutExternalWorkProfileSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        profile = self.queryset.get_or_none(email=ser.validated_data['email'])

        job_interested_in = JobAdvert.nodes.get_or_none(uid=ser.validated_data['interested_in'].hex)
        uploaded_documents = ser.validated_data.get('uploaded_documents', [])

        if profile is None:
            profile = ser.create(ser.validated_data)

        Mailer.express_interest(profile, job_interested_in, uploaded_documents)

        return Response()

    @action(methods=['post'], detail=False)
    def interested(self, request):
        ser = ExternalWorkProfileCreatorSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        profile = self.queryset.get_or_none(email=ser.validated_data['email'])

        job_interested_in = JobAdvert.nodes.get_or_none(uid=ser.validated_data['interested_in'].hex)
        uploaded_documents = ser.validated_data.get('uploaded_documents', [])

        if profile:

            # retain internal notes instead of replacing
            ser.validated_data['notes'] += '\n'+profile.notes

            ser.update(profile, ser.validated_data)
        else:
            profile = ser.create(ser.validated_data)

        Mailer.express_interest(profile, job_interested_in, uploaded_documents)

        return Response()