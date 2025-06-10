from django.db import models
from django.contrib.auth.models import User

def update_check_points(day):
    check_points = {
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

    for key in check_points:
        if int(key) <= day:
            check_points[key] = "true"

    return check_points

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

class Blog(models.Model):
    blog_name = models.CharField(max_length=500)
    blog_content = models.TextField()
    blog_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)  
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="blog", 
        default=1  
    )
    last_updated = models.DateTimeField(auto_now=True) 

class OneTimeEvent(models.Model):
    event_name = models.CharField(max_length=50)
    event_details = models.TextField()
    start_date = models.DateTimeField()
    is_high_importance = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    event_history = models.TextField(default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)  
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="one_time_event", 
        default=1  
    )
    last_updated = models.DateTimeField(auto_now=True) 

class StudyScope(models.Model):
    study_scope = models.JSONField(default=get_default_study_scope)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="study_scope", 
        default=1  
    )
    last_updated = models.DateTimeField(auto_now=True) 

class SubjectType(models.Model):
    type = models.CharField(max_length=20)
    category = models.CharField(max_length=20, default="SDE_Interview")
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="subject_type", 
        default=1  
    )
    created_at = models.DateTimeField(auto_now_add=True)   

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
    study_scope_id = models.ForeignKey(
        StudyScope,
        on_delete=models.CASCADE,
        related_name="study_scope_model", 
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
    subject_type = models.CharField(max_length = 50)
    importance_level = models.SmallIntegerField(default=1)
    in_half_year_repetition = models.BooleanField(default=False)
    question = models.TextField(default="N/A")
    record_details = models.TextField(default="N/A")
    record_neighbor = models.CharField(max_length=100, default="N/A")
    next_study_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)
    current_learning_session = models.BooleanField(default=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="memo_records", 
        default=1  
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.record_details
