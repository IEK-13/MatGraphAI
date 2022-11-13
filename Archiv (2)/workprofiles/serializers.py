from rest_framework import serializers

from core.models import Canton, JobCategory
from core.serializers import CantonSerializer
from graphutils.serializers import LabeledDjangoNodeSerializer, QuotaSerializer, UploadedDocuments
from jobs.models import CompanySize
from skills.models.education import Subject
from workprofiles.models import ExternalWorkProfile, WorkProfile
from skills.models.base import PersonalityType
from graphutils.helpers import connect_all, relation_to_internal_value
from skills.models.ontology import OntologyOccupation
from skills.models.skills import Skill
from skills.serializers import PersonalityTypeSerializer, SkillSerializer


class CVItemSerializer(serializers.Serializer):

    since = serializers.DateField(required=False)
    until = serializers.DateField(required=False)

    title = serializers.CharField(required=True)

class UserSkillSerializer(SkillSerializer):

    level = serializers.IntegerField(
        min_value=1,
        max_value=4,
        default=1,
        write_only=True
    )

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['level'] = self.root.instance.skills.relationship(instance).level
        return repr


class UserOccupationSerializer(CVItemSerializer):

    uid = serializers.UUIDField()

    company = serializers.CharField(required=False)
    description = serializers.CharField(required=False)


class UserEducationSerializer(CVItemSerializer):

    uid = serializers.UUIDField()

    school = LabeledDjangoNodeSerializer(required=False)
    degree = LabeledDjangoNodeSerializer(required=False)


class WorkProfileApplicationInfoSerializer(serializers.Serializer):

    def to_representation(self, instance):

        from users.models import ScramblUser

        user = ScramblUser.objects.get(id=instance.user)
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_url': instance.profile_url,
            'email': user.email
        }

class WorkProfileSerializer(serializers.Serializer):

    class Meta:
        model = WorkProfile

    occupations = UserOccupationSerializer(many=True, required=False)

    personality_types = PersonalityTypeSerializer(
        many=True,
        required=True
    )
    skills = UserSkillSerializer(
        many=True,
        required=True
    )

    cantons = CantonSerializer(
        many=True,
        required=False
    )
    job_categories = LabeledDjangoNodeSerializer(
        many=True,
        required=False
    )
    company_sizes = LabeledDjangoNodeSerializer(
        many=True,
        required=False
    )
    quota = QuotaSerializer(
        required=True
    )
    open_for_remote_work = serializers.BooleanField(
        default=True
    )

    educations = UserEducationSerializer(
        required=False,
        many=True,
        write_only=True
    )

    # frontend might pass the uid of an external profile that is being claimed
    externalProfileSourceUID = serializers.UUIDField(required=False, allow_null=True, write_only=True)

    def to_internal_value(self, data):

        data = super().to_internal_value(data)

        relation_to_internal_value(data, 'skills', Skill, add_attributes=['level'])
        relation_to_internal_value(data, 'personality_types', PersonalityType)
        relation_to_internal_value(data, 'company_sizes', CompanySize)
        relation_to_internal_value(data, 'cantons', Canton)
        relation_to_internal_value(data, 'job_categories', JobCategory)

        educations = []
        for edu in data['educations']:
            subject = Subject.nodes.get(uid=edu['uid'].hex)
            setattr(subject, 'title', edu['title'])
            if 'school' in edu:
                setattr(subject, 'school', edu['school']['uid'].hex)
            else:
                setattr(subject, 'school', None)
            if 'degree' in edu:
                setattr(subject, 'degree', edu['degree']['uid'].hex)
            else:
                setattr(subject, 'degree', None)
            educations.append(subject)
        data['educations'] = educations

        occupations = []
        for occ in data['occupations']:
            node = OntologyOccupation.nodes.get(uid=occ['uid'].hex)
            setattr(node, 'title', node.label) # TODO: company, description, title, since, until
            occupations.append(node)
        data['occupations'] = occupations

        return data

    def create(self, validated_data):

        profile = WorkProfile()

        if 'request' in self.context:
            if self.context['request'].user.is_authenticated:
                profile.user = self.context['request'].user.id.hex

        return self.update(profile, validated_data)

    def update(self, instance, validated_data):

        skills = validated_data.pop('skills')
        personality_types = validated_data.pop('personality_types')
        company_sizes = validated_data.pop('company_sizes', [])
        cantons = validated_data.pop('cantons')
        job_categories = validated_data.pop('job_categories')
        educations = validated_data.pop('educations')
        occupations = validated_data.pop('occupations')

        quota = validated_data.pop('quota')
        validated_data['min_quota'] = quota['min']
        validated_data['max_quota'] = quota['max']

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        connect_all(instance.personality_types, personality_types)
        connect_all(instance.company_sizes, company_sizes)
        connect_all(instance.cantons, cantons)
        connect_all(instance.job_categories, job_categories)

        instance.educations.disconnect_all()
        for edu in educations:
            instance.educations.connect(edu, {'school': edu.school, 'title': edu.title, 'degree': edu.degree}) # TODO: since, until

        instance.occupations.disconnect_all()
        for occ in occupations:
            instance.occupations.connect(occ, {'title': occ.title}) # TODO: since, until, description, company

        instance.skills.disconnect_all()
        for skill in skills:
            if hasattr(skill, 'level'):
                instance.skills.connect(skill, {'level': skill.level})
            else:
                instance.skills.connect(skill)

        return instance

    def get_occupations(self, instance):
        return UserEducationSerializer(instance.get_occupations(), many=True).data

    def get_educations(self, instance):
        return UserEducationSerializer(instance.get_educations(), many=True).data

    def to_representation(self, instance):
        self.fields['occupations'] = serializers.SerializerMethodField()
        self.fields['educations'] = serializers.SerializerMethodField()
        repr = super().to_representation(instance)

        return repr


class WorkProfileResultSerializer(serializers.Serializer):

    quota = QuotaSerializer()
    cantons = CantonSerializer(many=True)


class CandidateMatchSerializer(serializers.Serializer):

    details = serializers.SerializerMethodField()
    score = serializers.FloatField()
    skill_overlap = serializers.SerializerMethodField()

    # optional, only for logged in staff members
    full_name = serializers.CharField(required=False)

    def get_skill_overlap(self, match):
        return match['skill_overlap']

    def get_details(self, match):
        return WorkProfileResultSerializer(match['profile']).data

class ExternalWorkProfileSerializer(WorkProfileSerializer):

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    email = serializers.EmailField(required=True)

    notes = serializers.CharField(default="")

    def create(self, validated_data):

        profile = ExternalWorkProfile()

        if 'request' in self.context:
            if self.context['request'].user.is_authenticated:
                profile.user = self.context['request'].user.id.hex

        return self.update(profile, validated_data)


class ExternalWorkProfileCreatorSerializer(ExternalWorkProfileSerializer):

    uploaded_documents = UploadedDocuments(required=True, many=True)

    interested_in = serializers.UUIDField(required=True)

    def create(self, validated_data):
        validated_data.pop('uploaded_documents')
        validated_data.pop('interested_in')

        return super().create(validated_data)

class ExpressInterestWithoutExternalWorkProfileSerializer(serializers.Serializer):

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    email = serializers.EmailField(required=True)

    phone_number = serializers.CharField(required=False)

    notes = serializers.CharField(default="")

    type = serializers.CharField(default='external')

    uploaded_documents = UploadedDocuments(required=True, many=True)

    interested_in = serializers.UUIDField(required=True)

    def create(self, validated_data):

        profile = ExternalWorkProfile()
        return self.update(profile, validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('uploaded_documents')
        validated_data.pop('interested_in')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
