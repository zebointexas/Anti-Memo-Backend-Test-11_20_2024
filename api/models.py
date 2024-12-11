from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from django.utils import timezone

def get_default_check_points():
    return {
        "1": "false",
        "2": "false",
        "4": "false",
        "8": "false",
        "15": "false",
        "30": "false",
        "60": "false",
        "90": "false",
        "120": "false",
        "180": "false",
        "240": "false",
        "300": "false",
        "420": "false",
        "540": "false",
        "660": "false",
        "840": "false", 
        "1020": "false",
        "1200": "false"
    }

def get_default_study_scope():
    return {
        "subject_type": "all",
        "category": "all"
    }

class StudyScope(models.Model):
    study_scope = models.JSONField(default=get_default_study_scope)
    last_updated = models.DateTimeField(auto_now=True) 

class SubjectType(models.Model):
    type = models.CharField(max_length=20)
    category = models.CharField(max_length=20, default="Default Category")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subject_type")
    created_at = models.DateTimeField(auto_now_add=True)  # 记录创建时间

    def __str__(self):
        return self.type
    
# Note Model
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

class StudyPlan(models.Model):
    soft_reset_date = models.DateTimeField(auto_now_add=True)
    check_points = models.JSONField(default=get_default_check_points)
    last_updated = models.DateTimeField(auto_now=True)

class StudyHistory(models.Model):
    study_history = models.TextField()   
    study_days_count = models.SmallIntegerField(default=1)
    record_details_change_history = models.TextField(default="") 
    last_updated = models.DateTimeField(auto_now=True)

class MemoRecord(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="memo_records", 
        default=1  
    )
    study_history_id = models.ForeignKey(
        StudyHistory,
        on_delete=models.CASCADE,
        related_name="study_history_model", 
        default=1
    )
    study_plan_id = models.ForeignKey(
        StudyPlan,
        on_delete=models.CASCADE,
        related_name="study_plan_model",
        default=1
    )
    subject_type = models.CharField(max_length = 20)
    importance_level = models.SmallIntegerField(default=1)
    in_half_year_repetition = models.BooleanField(default=False)
    record_details = models.TextField()
    record_neighbor = models.CharField(max_length=100, default="N/A")
    next_study_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.record_details

# OneTimeEvent Model
class OneTimeEvent(models.Model):
    event_Id = models.SmallIntegerField()
    event_details = models.TextField()
    start_date = models.DateTimeField()
    retain_length = models.SmallIntegerField()
    is_done = models.BooleanField()
