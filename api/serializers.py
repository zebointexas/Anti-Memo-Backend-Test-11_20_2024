from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class SubjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectType
        fields = ['id', 'type', 'category', 'created_at', 'author']
        extra_kwargs = {"author": {"read_only": True}}

    def create(self, validated_data):
        return SubjectType.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}

class StudyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPlan
        fields = ["id", "soft_reset_date", "check_points", "last_updated"]

class StudyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyHistory
        fields = ["id", "study_history", "study_days_count", "record_details_change_history", "last_updated"]
 
class MemoRecordSerializer(serializers.ModelSerializer):
    study_plan_id = StudyPlanSerializer(read_only=True)
    study_history_id = StudyHistorySerializer(read_only=True)

    class Meta:
        model = MemoRecord
        fields = [
            "id",
            "subject_type",
            "importance_level",
            "author",
            "study_history_id",
            "study_plan_id",
            "in_half_year_repetition",
            "record_details",
            "record_neighbor",
            "next_study_time",
            "is_activate",
            "created_at"
        ]
        extra_kwargs = {
            "author": {"read_only": True},  # 'author' should be set by the user
            "study_plan_id": {"read_only": True},  # Read-only, but this could also be set manually if necessary
            "study_history_id": {"read_only": True},  # Same for study_history, read-only
            "subject_type": {"default": "Algo"},
            "record_neighbor": {"default": "N/A"},
        }

    def create(self, validated_data):
        study_plan = validated_data.get('study_plan_id', None)
        study_history = validated_data.get('study_history_id', None)
        
        if study_plan is None:
            raise serializers.ValidationError("Study Plan is required")
        
        if study_history is None:
            raise serializers.ValidationError("Study History is required")
        
        return MemoRecord.objects.create(**validated_data)

class OneTimeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneTimeEvent
        fields = [
            "id",
            "event_details",
            "start_date",
            "retain_length",
            "is_done",
        ]


