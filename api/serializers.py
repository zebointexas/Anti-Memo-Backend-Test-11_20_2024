from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, MemoRecord, OneTimeEvent

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

# Memo Record Serializer
class MemoRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoRecord
        fields = [
            "record_Id",
            "subject_Type",
            "importance_Level",
            # "author",
            # "memo_History",
            # "nominal_start_date",
            # "Study_Check_Points",
            # "in_half_year_repetition",
            "record_Details",
            # "recordNeighbor",
        ]
        extra_kwargs = {
            "author": {"read_only": True},
            "subject_Type": {"default": "Algo"},
        }

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