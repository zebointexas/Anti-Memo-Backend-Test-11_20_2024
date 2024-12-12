import logging
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models import *
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import localtime, now
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response 
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse

###########################################################################
########################################################################### Methods 
###########################################################################

         
                                          
 
def get_last_word(eachLine):
    words = eachLine.strip().split()
    if not words:
        return None
    return words[-1]

def roll_back_check_point(updated_day, roll_back_count, soft_reset_date, next_study_day, check_points):
    
    index = settings.CHECK_POINTS.index(updated_day)
    soft_reset_date = timezone.now() - settings.CHECK_POINTS[index - roll_back_count]
    next_study_day = soft_reset_date + settings.CHECK_POINTS[index - roll_back_count + 1]
     
def soft_reset(soft_reset_date, next_study_time): 
    soft_reset_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) 
    next_study_time = soft_reset_date

def next_study_time_normal_update(soft_reset_date, updated_day, memo_record): 
    index = settings.CHECK_POINTS.index(updated_day)
    if memo_record.in_half_year_repetition or index + 1 == len(settings.CHECK_POINTS): 
       memo_record.in_half_year_repetition = True
       next_study_time = memo_record.next_study_time + timedelta(days=182) 
    else: 
       next_study_time = soft_reset_date + timedelta(days=(settings.CHECK_POINTS[index + 1]))

###################### days handler 
######################

def handle_day_1(updated_day, soft_reset_date, check_points, gap_days, memo_record): 
    soft_reset(soft_reset_date, memo_record.next_study_time)     

def handle_day_2_or_4(updated_day, soft_reset_date, check_points, gap_days, memo_record):
    if gap_days == 1: 
       roll_back_check_point(updated_day, 1, soft_reset_date, memo_record.next_study_time, check_points)
    else: 
       soft_reset(soft_reset_date, memo_record.next_study_time)   

def handle_day_8_or_15(updated_day, soft_reset_date, check_points, gap_days, memo_record):
    if gap_days == 1: 
       roll_back_check_point(updated_day, 1, soft_reset_date, memo_record.next_study_time, check_points)
    if gap_days in (2,3): 
       roll_back_check_point(updated_day, 2, soft_reset_date, memo_record.next_study_time, check_points)       
    else: 
       soft_reset(soft_reset_date, memo_record.next_study_time)   

def handle_day_30_or_60(updated_day, soft_reset_date, check_points, gap_days, memo_record):
    if gap_days in (1,2,3): 
       roll_back_check_point(updated_day, 1, soft_reset_date, memo_record.next_study_time, check_points)
    if gap_days in (4,5,6,7,8): 
       roll_back_check_point(updated_day, 2, soft_reset_date, memo_record.next_study_time, check_points)       
    if gap_days in (9,10,11,12): 
       roll_back_check_point(updated_day, 3, soft_reset_date, memo_record.next_study_time, check_points)       
    if gap_days in (13,14,15,16): 
       roll_back_check_point(updated_day, 4, soft_reset_date, memo_record.next_study_time, check_points)              
    else: 
       soft_reset(soft_reset_date, memo_record.next_study_time)    

def handle_day_90_or_120_or_180(updated_day, soft_reset_date, check_points, gap_days, memo_record):   
    if 1 <= gap_days <= 4: 
       roll_back_check_point(updated_day, 1, soft_reset_date, memo_record.next_study_time, check_points)
    if 5 <= gap_days <= 10: 
       roll_back_check_point(updated_day, 2, soft_reset_date, memo_record.next_study_time, check_points)       
    if 11 <= gap_days <= 16: 
       roll_back_check_point(updated_day, 3, soft_reset_date, memo_record.next_study_time, check_points)       
    if 16 <= gap_days <= 22:  
       roll_back_check_point(updated_day, 5, soft_reset_date, memo_record.next_study_time, check_points)              
    else: 
       soft_reset(soft_reset_date, memo_record.next_study_time)      

def handle_day_240_or_300_or_420(updated_day, soft_reset_date, check_points, gap_days, memo_record):  
    if 1 <= gap_days <= 5: 
       roll_back_check_point(updated_day, 1, soft_reset_date, memo_record.next_study_time, check_points)
    if 6 <= gap_days <= 13: 
       roll_back_check_point(updated_day, 2, soft_reset_date, memo_record.next_study_time, check_points)       
    if 14 <= gap_days <= 21: 
       roll_back_check_point(updated_day, 3, soft_reset_date, memo_record.next_study_time, check_points)       
    if 22 <= gap_days <= 36:  
       roll_back_check_point(updated_day, 5, soft_reset_date, memo_record.next_study_time, check_points)              
    else: 
       soft_reset(soft_reset_date, memo_record.next_study_time)   

def handle_day_rest_of_all(updated_day, soft_reset_date, check_points, gap_days, memo_record):  
    if 1 <= gap_days <= 15: 
       roll_back_check_point(updated_day, 1, soft_reset_date, memo_record.next_study_time, check_points)
    if 16 <= gap_days <= 30: 
       roll_back_check_point(updated_day, 2, soft_reset_date, memo_record.next_study_time, check_points)       
    if 31 <= gap_days <= 45: 
       roll_back_check_point(updated_day, 3, soft_reset_date, memo_record.next_study_time, check_points)       
    if 46 <= gap_days <= 60:  
       roll_back_check_point(updated_day, 5, soft_reset_date, memo_record.next_study_time, check_points)              
    else: 
       soft_reset(soft_reset_date, memo_record.next_study_time)   

def update_next_study_time_for_study_plan(memo_record, updated_day): 
    if memo_record.in_half_year_repetition == True: 
        memo_record.next_study_time = memo_record.study_history.last_updated + relativedelta(months=6)
    else: 
        soft_reset_date = memo_record.study_plan.soft_reset_date
        expected_day = (timezone.now() - soft_reset_date).days + 1 

        check_points = memo_record.study_history.check_points
        gap_days = (updated_day - expected_day).days

        if gap_days == 0: 
           next_study_time_normal_update(soft_reset_date, updated_day, memo_record)

        key_handler_map = {
            "1": handle_day_1,
            "2": handle_day_2_or_4,
            "4": handle_day_2_or_4,
            "8": handle_day_8_or_15,
            "15": handle_day_8_or_15,
            "30": handle_day_30_or_60,
            "60": handle_day_30_or_60,
            "90": handle_day_90_or_120_or_180,
            "120": handle_day_90_or_120_or_180,
            "180": handle_day_90_or_120_or_180,
            "240": handle_day_240_or_300_or_420,
            "300": handle_day_240_or_300_or_420,
            "420": handle_day_240_or_300_or_420,
            "540": handle_day_rest_of_all,
            "660": handle_day_rest_of_all,
            "840": handle_day_rest_of_all,
            "1020": handle_day_rest_of_all,
            "1200": handle_day_rest_of_all,
        }

        handler = key_handler_map.get(expected_day)
        handler(updated_day, soft_reset_date, check_points, gap_days, memo_record)
         
def update_study_plan(memo_record):
    check_points = memo_record.study_plan.check_points
    for updated_day, value in check_points.items():
        if value == "false":
            check_points[updated_day] = "true"
            memo_record.study_plan.check_points = check_points
            memo_record.study_plan.save()
            update_next_study_time_for_study_plan(memo_record, updated_day)
            return False
    memo_record.in_half_year_repetition = True
             
def check_study_history_and_update_next_study_time(memo_record, last_five_lines, study_history_last_updated_time):
    
    remember_count = 0; 

    if not last_five_lines: 
        return

    for eachLine in reversed(last_five_lines):
        if eachLine.strip():                 
            last_word = get_last_word(eachLine)
            if last_word == 'Remember':
                remember_count += 1
            if last_word == 'Forget':
                break
 
    wait_time = 0

    if remember_count == 1: 
       wait_time = 5
    elif remember_count == 2: 
       wait_time = 15
    elif remember_count == 3:    
       wait_time = 30
    elif remember_count == 4:  
       wait_time = 30  
    elif remember_count == 5:  
      wait_time = 30
    elif remember_count == 6:  
      wait_time = 60 
    elif remember_count == 7:  
       update_study_plan(memo_record)

    memo_record.next_study_time = study_history_last_updated_time + timedelta(minutes=wait_time)
    
###########################################################################
########################################################################### classes 
########################################################################### 

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)
 
class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


# Create User View
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


####################################################################################
####################################################################################
#################################################################################### MemoRecords
####################################################################################
####################################################################################


# MemoRecord List and Create View
class MemoRecordList(generics.ListCreateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    # subjects = [
    #     {"type": "Java", "category": "SDE_Interview", "author_id": 1},
    #     {"type": "Python", "category": "SDE_Interview", "author_id": 1},
    #     {"type": "Algo", "category": "SDE_Interview", "author_id": 1},
    #     {"type": "System_Design", "category": "SDE_Interview", "author_id": 1},
    #     {"type": "OOD", "category": "SDE_Interview", "author_id": 1},
    #     {"type": "BQ", "category": "SDE_Interview", "author_id": 1},
    #     {"type": "Linux", "category": "SRE", "author_id": 1},
    #     {"type": "Network", "category": "SRE", "author_id": 1},
    #     {"type": "General_IT", "category": "IT", "author_id": 1},
    #     {"type": "French", "category": "Language", "author_id": 1},
    #     {"type": "English", "category": "Language", "author_id": 1},
    #     {"type": "Friends_Info", "category": "Social", "author_id": 1},
    #     {"type": "Math", "category": "Mathematics", "author_id": 1},
    #     {"type": "Machine_Learning", "category": "AI", "author_id": 1}
    # ]

    # # 插入数据
    # for subject in subjects:
    #     # 获取 `author` 实例，确保用户存在
    #     try:
    #         author = User.objects.get(id=subject["author_id"])
    #     except User.DoesNotExist:
    #         print(f"User with ID {subject['author_id']} does not exist. Skipping {subject['type']}.")
    #         continue

    #     # 使用 `get_or_create` 避免重复插入
    #     subject_type, created = SubjectType.objects.get_or_create(
    #         type=subject["type"],
    #         category=subject["category"],
    #         author=author  # 绑定作者
    #     )
    #     if created:
    #         print(f"Created: {subject['type']}")
    #     else:
    #         print(f"Already exists: {subject['type']}")

    def get_queryset(self):
        user = self.request.user
        memo_records = MemoRecord.objects.filter(author=user).select_related('study_plan_id', 'study_history_id')
        memo_records = list(memo_records)             

        print("------------------------------------------------------------ total records " + str(len(memo_records))); 

        for record in memo_records[:]:
            if record.study_history_id: 
                study_history_content = record.study_history_id.study_history   
                study_history_last_updated_time = record.study_history_id.last_updated
                study_history_lines = study_history_content.splitlines()
                last_five_lines = study_history_lines[-7:]  
                check_study_history_and_update_next_study_time(record, last_five_lines, study_history_last_updated_time)
                
                print( "------------- record.next_study_time - timezone.now() = " + str(record.next_study_time - timezone.now()) ); 

                if record.next_study_time > timezone.now(): 
                    memo_records.remove(record)
        
        return memo_records
 
class MemoRecordCreate(generics.ListCreateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        if serializer.is_valid():
 
            # study_scope = StudyScope.objects.create(
            #     study_scope=get_default_study_scope()
            # )
 
            # study_plan = StudyPlan.objects.create(
            #     check_points=get_default_check_points()
            # )
 
            # study_history = StudyHistory.objects.create(
            #     study_history="Initial Study History",
            #     study_days_count="1",
            #     record_details_change_history="Initial History Details"
            # )
            user = self.request.user

            try:
                study_scope = StudyScope.objects.get(author=user)
            except StudyScope.DoesNotExist:
                # 如果不存在，则创建一个新的 StudyScope
                study_scope = StudyScope.objects.create(
                    study_scope=get_default_study_scope(),
                    author=user
                )

            # 创建 StudyPlan 和 StudyHistory
            study_plan = StudyPlan.objects.create(
                check_points=get_default_check_points()
            )
            study_history = StudyHistory.objects.create(
                study_history="Initial Study History",
                study_days_count="1",
                record_details_change_history="Initial History Details"
            )
 
            memo_record = serializer.save(author=self.request.user, study_plan_id=study_plan, study_history_id=study_history, study_scope_id = study_scope);
        else:
            print(serializer.errors)
 

class MemoRecordDelete(generics.DestroyAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)

    def destroy(self, request, *args, **kwargs):
        # 获取 MemoRecord 实例
        instance = self.get_object()

        # 获取关联的 StudyHistory 和 StudyPlan
        study_history = instance.study_history_id
        study_plan = instance.study_plan_id

        # 删除 MemoRecord
        self.perform_destroy(instance)
        study_history.delete()
        study_plan.delete()
 
        return Response(
            {"message": "MemoRecord and related StudyHistory and StudyPlan deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )                
 
class SubjectTypeList(generics.ListCreateAPIView):
    queryset = SubjectType.objects.all()
    serializer_class = SubjectTypeSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset().values('id', 'type', 'category')
    #     return Response(queryset)
    
    def get_queryset(self):
        user = self.request.user
        return SubjectType.objects.filter(author=user)

# class SubjectTypeList(generics.ListCreateAPIView):
#     serializer_class = SubjectTypeSerializer
#     permission_classes = [IsAuthenticated]

#     def list(self, request, *args, **kwargs):
#         queryset = SubjectType.objects.filter(author=request.user)
#         return Response(queryset)    

class SubjectTypeCreate(generics.ListCreateAPIView):
    serializer_class = SubjectTypeSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        if serializer.is_valid():
           serializer.save(author=self.request.user);
        else:
            print(serializer.errors)

# 删除视图
class SubjectTypeDelete(generics.DestroyAPIView):
    serializer_class = SubjectTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SubjectType.objects.filter(author=user)
        
class MemoRecordUpdateStudyHistory(generics.UpdateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
 
            instance = serializer.instance
            remember_status = self.request.headers.get('Remember-Status', 'default_status')
            current_date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            study_history_instance = instance.study_history_id
            
            if study_history_instance:
                study_history = study_history_instance.study_history
            else:
                study_history = ''

            updated_study_history = f"{study_history}\nReviewed on: {current_date}    |    {remember_status}"
            instance.study_history = updated_study_history
     
            study_history_instance.study_history = updated_study_history
            study_history_instance.save() 

            print("Study history updated successfully.")
        else:
            print(serializer.errors)

class MemoRecordUpdateRecordDetails(generics.UpdateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            instance = serializer.instance
            record_details = self.request.data.get('record_details', None)
            instance.record_details = record_details
            instance.save()
        else:
            print(serializer.errors)

class StudyScopeUpdate(generics.UpdateAPIView):
    serializer_class = StudyScopeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return StudyScope.objects.filter(author=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            instance = serializer.instance
            updated_study_scope = self.request.data
            instance.study_scope = updated_study_scope
            instance.save()
        else:
            print(serializer.errors)