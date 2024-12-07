from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from django.utils import timezone

# Enum for Subject Type
class SubjectType(Enum):
    Java = "Java"
    Python = "Python"
    Algo = "Algo"
    System_Design = "System_Design"
    OOD = "ODD"
    Linux = "Linux"
    Network = "Network"
    General_IT = "General_IT"
    BQ = "BQ"
    French = "French"
    English = "English"
    Friends_Info = "Friends_Info"
    Math = "Math"
    Machine_Learning = "Machine_Learning"

# Note Model
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

def get_default_study_check_points():
    return {
        "Day_1": "false",
        "Day_2": "false",
        "Day_4": "false",
        "Day_8": "false",
        "Day_15": "false",
        "Day_30": "false",
        "Day_60": "false",
        "Day_90": "false",
        "Day_120": "false",
        "Day_180": "false",
        "Day_300": "false",
        "Day_480": "false",
        "Day_640": "false",
        "Day_End": "false",
    }

class StudyPlan(models.Model):
    nominal_start_date_for_progress_calculation = models.DateTimeField(default=timezone.now)
    study_check_points = models.JSONField(default=get_default_study_check_points)
    last_updated = models.DateTimeField(auto_now=True)

class StudyHistory(models.Model):
    study_history = models.TextField()   
    study_days_count = models.SmallIntegerField(default=1)
    record_details_change_history = models.TextField(default="") 
    last_updated = models.DateTimeField(auto_now=True)

class MemoRecord(models.Model):
    subject_type = models.CharField(
        max_length=20, 
        choices=[(tag.value, tag.name) for tag in SubjectType], 
        default=SubjectType.Algo.value,
    )
    importance_level = models.SmallIntegerField(default=1)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="memo_records", 
        default=1  
    )
    study_history = models.ForeignKey(
        StudyHistory,
        on_delete=models.CASCADE,
        related_name="study_history_model", 
        default=1
    )
    nominal_start_date_for_progress_calculation = models.DateTimeField(default=timezone.now)
    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.CASCADE,
        related_name="study_plan_model",
        default=1
    )
    in_half_year_repetition = models.BooleanField(default=False)
    record_details = models.TextField()
    record_neighbor = models.CharField(max_length=100, default="N/A")
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
