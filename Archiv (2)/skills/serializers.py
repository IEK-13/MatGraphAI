from rest_framework import serializers
from skills.models.skills import Skill


class PersonalityTypeSerializer(serializers.Serializer):

    code = serializers.CharField()
    label = serializers.CharField(read_only=True)


class OccupationAutocompleteSerializer(serializers.Serializer):

    label = serializers.CharField(read_only=True)
    uid = serializers.UUIDField()


class OntologyOccupationAutocompleteSerializer(serializers.Serializer):

    label = serializers.CharField(read_only=True)
    id = serializers.IntegerField(source='ontology_id')


class SkillSerializer(serializers.Serializer):

    uid = serializers.UUIDField(required=False)
    label = serializers.CharField()
    type = serializers.CharField()

    def create(self, validated_data):

        skill = Skill()
        skill.user_skill = True

        return self.update(skill, validated_data)

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return instance.save()


class CourseSerializer(serializers.Serializer):

    uid = serializers.UUIDField()
    subject = serializers.SerializerMethodField()
    degree = serializers.SerializerMethodField()

    def get_subject(self, course):
        return course.subject.single().label

    def get_degree(self, course):
        return course.degree.single().label
