from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id", 
            "blog_name",
            "blog_content",
            "blog_type", 
            "created_at", 
            "author", 
            "last_updated"
        ]
        extra_kwargs = {
            "author": {"read_only": True},  # 作者由后端自动设置
            "created_at": {"read_only": True},  # 自动生成
            "last_updated": {"read_only": True},  # 自动生成
        }

class OneTimeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneTimeEvent
        fields = [
            "id", 
            "event_name", 
            "event_details", 
            "start_date", 
            "is_high_importance", 
            "is_done", 
            "event_history", 
            "created_at", 
            "author", 
            "last_updated"
        ]
        extra_kwargs = {
            "author": {"read_only": True},  # 作者由后端自动设置
            "created_at": {"read_only": True},  # 自动生成
            "last_updated": {"read_only": True},  # 自动生成
        }

    # def create(self, validated_data):
    #     return OneTimeEvent.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     for field, value in validated_data.items():
    #         setattr(instance, field, value)
    #     instance.save()
    #     return instance

class StudyScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyScope
        fields = ['id', 'study_scope', 'author', 'last_updated']

    def create(self, validated_data):
        return StudyScope.objects.create(**validated_data)

class SubjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectType
        fields = ['id', 'type', 'category', 'created_at']

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
    study_scope_id = StudyScopeSerializer(read_only=True)

    class Meta:
        model = MemoRecord
        fields = [
            "id",
            "study_scope_id",
            "study_history_id",
            "study_plan_id",
            "subject_type",
            "importance_level",
            "in_half_year_repetition",
            "question",
            "record_details",
            "record_neighbor",
            "next_study_time",
            "author",
            "is_activate",
            "current_learning_session",
            "created_at"
        ]
        extra_kwargs = {
            "author": {"read_only": True},  # 'author' should be set by the user
            "study_scope_id": {"read_only": True},  # Read-only, but this could also be set manually if necessary
            "study_plan_id": {"read_only": True},  # Read-only, but this could also be set manually if necessary
            "study_history_id": {"read_only": True},  # Same for study_history, read-only
            "subject_type": {"default": "Algo"},
            "record_neighbor": {"default": "N/A"},
        }

    def create(self, validated_data):
        study_scope = validated_data.get('study_scope_id', None)
        study_plan = validated_data.get('study_plan_id', None)
        study_history = validated_data.get('study_history_id', None)
        
        if study_scope is None:
            raise serializers.ValidationError("Study Scope is required")

        if study_plan is None:
            raise serializers.ValidationError("Study Plan is required")
        
        if study_history is None:
            raise serializers.ValidationError("Study History is required")
        
        return MemoRecord.objects.create(**validated_data)