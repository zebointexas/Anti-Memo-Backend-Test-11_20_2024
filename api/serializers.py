from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, MemoRecord, OneTimeEvent, StudyPlan, StudyHistory

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Note Serializer
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}

class StudyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPlan
        fields = ["id", "nominal_start_date_for_progress_calculation", "study_check_points"]

# StudyHistory Serializer
class StudyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyHistory
        fields = ["id", "study_history", "study_days_count", "record_details_change_history", "last_updated"]

# MemoRecord Serializer
class MemoRecordSerializer(serializers.ModelSerializer):
    # Nested serializer for the related foreign keys
    study_plan = StudyPlanSerializer(read_only=True)
    study_history = StudyHistorySerializer(read_only=True)

    class Meta:
        model = MemoRecord
        fields = [
            "id",
            "subject_type",
            "importance_level",
            "author",
            "study_history",
            "nominal_start_date_for_progress_calculation",
            "study_plan",
            "in_half_year_repetition",
            "record_details",
            "record_neighbor",
            "is_activate",
            "created_at"
        ]
        extra_kwargs = {
            "author": {"read_only": True},  # 'author' should be set by the user
            "study_plan": {"read_only": True},  # Read-only, but this could also be set manually if necessary
            "study_history": {"read_only": True},  # Same for study_history, read-only
            "subject_type": {"default": "Algo"},
            "record_neighbor": {"default": "N/A"},
        }

    def create(self, validated_data):
        # Handle creating the MemoRecord instance with study_plan and study_history
        study_plan = validated_data.get('study_plan', None)
        study_history = validated_data.get('study_history', None)
        
        if study_plan is None:
            # If study_plan is required, raise an error or handle accordingly
            raise serializers.ValidationError("Study Plan is required")
        
        if study_history is None:
            # If study_history is required, raise an error or handle accordingly
            raise serializers.ValidationError("Study History is required")
        
        return MemoRecord.objects.create(**validated_data)

# One Time Event Serializer
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


