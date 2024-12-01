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

# Memo Record Model
class MemoRecord(models.Model):
    subject_Type = models.CharField(
        max_length=20, 
        choices=[(tag.value, tag.name) for tag in SubjectType], 
        default=SubjectType.Algo.value,
    )
    importance_Level = models.SmallIntegerField(default=1)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="memo_records", 
        default=1  
    )
    memo_History = models.TextField()    
    nominal_start_date = models.DateTimeField(default=timezone.now)
    Study_Check_Points = models.TextField(
        default=""" Day_1: false
                    Day_1_repeat: false
                    Day_2: false
                    Day_4: false
                    Day_8: false
                    Day_15: false
                    Day_30: false
                    Day_60: false
                    Day_90: false
                    Day_120: false
                    Day_180: false
                    Day_300: false
                    Day_480: false
                    Day_640: false
                    Day_End: false
                """
    )
    in_half_year_repetition = models.BooleanField(default=False)
    record_Details = models.TextField()
    recordNeighbor = models.CharField(max_length=100, default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record_Details

# OneTimeEvent Model
class OneTimeEvent(models.Model):
    event_Id = models.SmallIntegerField()
    event_details = models.TextField()
    start_date = models.DateTimeField()
    retain_length = models.SmallIntegerField()
    is_done = models.BooleanField()
