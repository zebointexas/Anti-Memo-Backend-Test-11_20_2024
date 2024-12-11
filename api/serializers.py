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

class StudyScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyScope
        fields = ['id', 'study_scope', 'last_updated']  # 需要序列化的字段

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
 
# class MemoRecordSerializer(serializers.ModelSerializer):
#     study_plan_id = StudyPlanSerializer(read_only=True)
#     study_history_id = StudyHistorySerializer(read_only=True)

#     class Meta:
#         model = MemoRecord
#         fields = [
#             "id",
#             "subject_type",
#             "importance_level",
#             "author",
#             "study_history_id",
#             "study_plan_id",
#             "in_half_year_repetition",
#             "record_details",
#             "record_neighbor",
#             "next_study_time",
#             "is_activate",
#             "created_at"
#         ]
#         extra_kwargs = {
#             "author": {"read_only": True},  # 'author' should be set by the user
#             "study_plan_id": {"read_only": True},  # Read-only, but this could also be set manually if necessary
#             "study_history_id": {"read_only": True},  # Same for study_history, read-only
#             "subject_type": {"default": "Algo"},
#             "record_neighbor": {"default": "N/A"},
#         }

#     def create(self, validated_data):
#         study_plan = validated_data.get('study_plan_id', None)
#         study_history = validated_data.get('study_history_id', None)
        
#         if study_plan is None:
#             raise serializers.ValidationError("Study Plan is required")
        
#         if study_history is None:
#             raise serializers.ValidationError("Study History is required")
        
#         return MemoRecord.objects.create(**validated_data)

class MemoRecordSerializer(serializers.ModelSerializer):
    # 嵌套相关模型的序列化器
    study_plan_id = StudyPlanSerializer(read_only=True)  # Read-only 如果您不打算在前端编辑
    study_history_id = StudyHistorySerializer(read_only=True)
    study_scope_id = StudyScopeSerializer(read_only=True)  # 允许在创建时填充或在后台选择
    
    author = UserSerializer(read_only=True)  # 仅显示与作者相关的数据，假设您有一个UserSerializer

    class Meta:
        model = MemoRecord
        fields = [
            "id",
            "study_scope_id",  # 关联的 StudyScope 序列化器
            "study_history_id",  # 关联的 StudyHistory 序列化器
            "study_plan_id",  # 关联的 StudyPlan 序列化器
            "subject_type",
            "importance_level",            
            "in_half_year_repetition",
            "record_details",
            "record_neighbor",
            "next_study_time",
            "is_activate",
            "author",  # 这个字段是只读的，会根据当前用户自动填充
            "created_at",
            "last_updated"
        ]
        extra_kwargs = {
            "author": {"read_only": True},  # 'author' 由当前登录用户自动设置，不允许在前端修改
            "study_scope_id": {"required": True},  # StudyScope 必须提供
            "study_plan_id": {"required": True},  # StudyPlan 必须提供
            "study_history_id": {"required": True},  # StudyHistory 必须提供
            "subject_type": {"default": "Algo"},
            "record_neighbor": {"default": "N/A"},
        }

    def create(self, validated_data):
        # 确保所有必要的字段都已提供
        study_scope = validated_data.get('study_scope_id', None)
        study_plan = validated_data.get('study_plan_id', None)
        study_history = validated_data.get('study_history_id', None)
        
        if study_scope is None:
            raise serializers.ValidationError("Study Scope is required")
        
        if study_plan is None:
            raise serializers.ValidationError("Study Plan is required")
        
        if study_history is None:
            raise serializers.ValidationError("Study History is required")
        
        # 创建 MemoRecord 实例
        return MemoRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # 更新 MemoRecord 实例，允许部分更新
        instance.study_scope_id = validated_data.get('study_scope_id', instance.study_scope_id)
        instance.study_plan_id = validated_data.get('study_plan_id', instance.study_plan_id)
        instance.study_history_id = validated_data.get('study_history_id', instance.study_history_id)
        instance.subject_type = validated_data.get('subject_type', instance.subject_type)
        instance.importance_level = validated_data.get('importance_level', instance.importance_level)
        instance.in_half_year_repetition = validated_data.get('in_half_year_repetition', instance.in_half_year_repetition)
        instance.record_details = validated_data.get('record_details', instance.record_details)
        instance.record_neighbor = validated_data.get('record_neighbor', instance.record_neighbor)
        instance.next_study_time = validated_data.get('next_study_time', instance.next_study_time)
        instance.is_activate = validated_data.get('is_activate', instance.is_activate)
        
        instance.save()
        return instance

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


