from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response 
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from django.db.models import Case, When, Value, IntegerField
import random
from django.http import FileResponse, HttpResponse  # Add FileResponse here
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required

###########################################################################
########################################################################### Methods 
###########################################################################

def download_db(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    if not os.path.exists(db_path):
        return HttpResponse("Database file not found.", status=404)
    response = FileResponse(
        open(db_path, 'rb'),
        as_attachment=True,
        filename='db.sqlite3'
    )
    
    print("--------------")
    
    return response

def exam_every_record(memo_records):

    memo_records = list(memo_records) 

    for record in memo_records[:]:

        if record.study_history_id: 
            study_history_content = record.study_history_id.study_history   
            study_history_last_updated_time = record.study_history_id.last_updated
            study_history_lines = study_history_content.splitlines()
            last_seven_lines = study_history_lines[-3:] 
 
            check_study_history_and_update_next_study_time(memo_records, record, last_seven_lines, study_history_last_updated_time)

    return memo_records


def filter_by_next_study_time(user): 

    memo_records = MemoRecord.objects.filter(author=user, next_study_time__lte= timezone.now(), is_activate=True, current_learning_session=True).select_related('study_plan_id', 'study_history_id', 'study_scope_id').order_by('next_study_time')
 
    return memo_records; 

def filter_by_study_scope(memo_records, user):

    try:
        study_scope = StudyScope.objects.get(author=user)
        study_scope_data = study_scope.study_scope  
    except StudyScope.DoesNotExist:
        return MemoRecord.objects.none()

    subject_types = study_scope_data.get('subject_types', [])
    categories = study_scope_data.get('categories', [])
 
    if subject_types:
        memo_records = memo_records.filter(subject_type__in=subject_types)
    if categories:
        subject_types = SubjectType.objects.filter(category__in=categories, author=user).values_list('type', flat=True)
        memo_records = memo_records.filter(subject_type__in=list(subject_types))
    
    return memo_records

def get_seleted_50_memo_records(memo_records, past_hours): 
    
    time_limit = timezone.now() - timedelta(hours=past_hours)
 
    # 1. 过滤出 "next_study_time" 在过去 past_hours 小时内的记录
    recent_records = [record for record in memo_records if record.next_study_time >= time_limit]
 
    # 2. 如果记录数量不到50个，就选择最早的记录来补充 （如果超过50，那就有多少就return多少）
    if len(recent_records) < 50:
        remaining_records = sorted([record for record in memo_records if record.next_study_time < time_limit], key=lambda x: x.next_study_time)

        # 补充不足的记录
        records_to_add = remaining_records[:50 - len(recent_records)]

        # 将补充的记录添加到 recent_records
        recent_records.extend(records_to_add)
    
    random.shuffle(recent_records)

    return recent_records[:50]

def get_last_word(eachLine):
    words = eachLine.strip().split()
    if not words:
        return None
    return words[-1]

def roll_back_check_point(revised_day, roll_back_count, memo_record): # 这里的逻辑很绕
    
    # CHECK_POINTS = (1, 2, 4, 8, 15, 30, 60, 90, 120, 180, 240, 300, 420, 540, 660, 840, 1020, 1200)
    #                             |           |
    index = settings.CHECK_POINTS.index(int(revised_day))  # 拿到 revised_day (变成True) 的 index

    index_after_rollback = index - roll_back_count

    day_after_rollback = settings.CHECK_POINTS[index_after_rollback] # rolled_back_day，等于，重新算之后，今天是day几
 
    study_plan_instance = memo_record.study_plan_id

    study_plan_instance.soft_reset_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=day_after_rollback - 1)
    
    study_plan_instance.check_points = update_check_points(day_after_rollback)

    study_plan_instance.save()
 
    memo_record.next_study_time = study_plan_instance.soft_reset_date + timedelta(days=( settings.CHECK_POINTS[index - roll_back_count + 1] - 1 ))

    memo_record.save()

    print("----> memo_record.saved")
     
def soft_reset(memo_record): 
    
    study_plan_instance = memo_record.study_plan_id
    study_plan_instance.soft_reset_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)  # put reset day to tomorrow, and start from tomorrow
    study_plan_instance.check_points = get_default_check_points()
    study_plan_instance.save()
    memo_record.next_study_time = study_plan_instance.soft_reset_date
    memo_record.save()

def next_study_time_normal_update(soft_reset_date, revised_day, memo_record): 

    print("--> now enter normal update")

    index = settings.CHECK_POINTS.index(int(revised_day))

    if memo_record.in_half_year_repetition or index + 1 == len(settings.CHECK_POINTS): 
       memo_record.in_half_year_repetition = True
       memo_record.next_study_time = memo_record.next_study_time + timedelta(days=182) 
    else: 
       memo_record.next_study_time = soft_reset_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta( days=(settings.CHECK_POINTS[index + 1] - 1) )
       print("--> now enter normal update --> memo_record.next_study_time updated = " + str(memo_record.next_study_time))
       memo_record.save()

###################### days handler 
######################
 
def handle_day_1(revised_day, gap_days, memo_record): 
    soft_reset(memo_record)     

def handle_day_2_or_4(revised_day, gap_days, memo_record):
    if gap_days == 1: 
       roll_back_check_point(revised_day, 1, memo_record)
    else: 
       soft_reset(memo_record)   

def handle_day_8_or_15(revised_day, gap_days, memo_record):
    print("---> now enter 8")
    if gap_days == 1: 
       print("---> now gap_days is 1")
       roll_back_check_point(revised_day, 1, memo_record)
    elif gap_days in (2,3): 
       roll_back_check_point(revised_day, 2, memo_record)       
    else: 
       soft_reset(memo_record)   

def handle_day_30_or_60(revised_day, gap_days, memo_record):
    if gap_days in (1,2,3): 
       roll_back_check_point(revised_day, 1, memo_record)
    elif gap_days in (4,5,6,7,8): 
       roll_back_check_point(revised_day, 2, memo_record)       
    elif gap_days in (9,10,11,12): 
       roll_back_check_point(revised_day, 3, memo_record)       
    elif gap_days in (13,14,15,16): 
       roll_back_check_point(revised_day, 4, memo_record)              
    else: 
       soft_reset(memo_record)    

def handle_day_90_or_120_or_180(revised_day, gap_days, memo_record):   

    print("----> now enter day 90 handler, and the gap_days = " + str(gap_days))

    if 1 <= gap_days <= 4: 
       roll_back_check_point(revised_day, 1, memo_record)
    elif 5 <= gap_days <= 10: 
       roll_back_check_point(revised_day, 2, memo_record)       
    elif 11 <= gap_days <= 16: 
       roll_back_check_point(revised_day, 3, memo_record)       
    elif 16 <= gap_days <= 22:  
       roll_back_check_point(revised_day, 5, memo_record)              
    else: 
       soft_reset(memo_record)      

def handle_day_240_or_300_or_420(revised_day, gap_days, memo_record):  
    if 1 <= gap_days <= 5: 
       roll_back_check_point(revised_day, 1, memo_record)
    elif 6 <= gap_days <= 13: 
       roll_back_check_point(revised_day, 2, memo_record)       
    elif 14 <= gap_days <= 21: 
       roll_back_check_point(revised_day, 3, memo_record)       
    elif 22 <= gap_days <= 36:  
       roll_back_check_point(revised_day, 5, memo_record)              
    else: 
       soft_reset(memo_record)   

def handle_day_rest_of_all(revised_day, gap_days, memo_record):  
    if 1 <= gap_days <= 15: 
       roll_back_check_point(revised_day, 1, memo_record)
    elif 16 <= gap_days <= 30: 
       roll_back_check_point(revised_day, 2, memo_record)       
    elif 31 <= gap_days <= 45: 
       roll_back_check_point(revised_day, 3, memo_record)       
    elif 46 <= gap_days <= 60:  
       roll_back_check_point(revised_day, 5, memo_record)              
    else: 
       soft_reset(memo_record)   

def update_next_study_time_for_study_plan(memo_record, revised_day): 
    if memo_record.in_half_year_repetition == True: 
        memo_record.next_study_time = memo_record.study_history.last_updated + relativedelta(months=6)
    else: 

        soft_reset_date = memo_record.study_plan_id.soft_reset_date

        today_day = (timezone.now()  - soft_reset_date).days + 1  # 因为，比如，今天 - 今天，其实是 0， 它这里要按照完整的一天，才算1天。
     
        gap = today_day - int(revised_day)

        # print("---> Program is working")

        # print("------> revised_day = " + str(revised_day))
        # print("------> today_day = " + str(today_day))
        # print("------> gap = " + str(gap))
        
        if gap <= 0: 
           print("--> Now gap <= 0 !!!")
           next_study_time_normal_update(soft_reset_date, revised_day, memo_record)
        else: 
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

            print("-------------------> revised_day = " + str(revised_day))

            handler = key_handler_map.get(revised_day)

            handler(revised_day, gap, memo_record)
         
def update_study_plan(memo_record):
    check_points = memo_record.study_plan_id.check_points
    for revised_day, value in check_points.items():
        if value == "false":
            check_points[revised_day] = "true"  
            memo_record.study_plan_id.check_points = check_points
            memo_record.study_plan_id.save()
            print("-----------> revised_day = " + revised_day)
            update_next_study_time_for_study_plan(memo_record, revised_day)
            return False
    memo_record.in_half_year_repetition = True
             
def check_study_history_and_update_next_study_time(all_memo_records, memo_record, last_seven_lines, study_history_last_updated_time):
    
    # print("--> now check history, and the id = " + str(memo_record.id))

    remember_count = 0; 

    if not last_seven_lines: 
        return

    for eachLine in reversed(last_seven_lines):

        # print(eachLine)

        if eachLine.strip():                 
            last_word = get_last_word(eachLine)
            if last_word == 'Remember':
                remember_count += 1
            else:
                break
 
    wait_time = 0

    # if(memo_record.subject_type == "Algo"):

    if remember_count == 0: 
            wait_time = 0
    elif remember_count == 1: 
            wait_time = 5
    elif remember_count == 2: 
            wait_time = 15
    elif remember_count == 3:  
            print("--> now print count 3")
            current_date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            study_history_instance = memo_record.study_history_id
            study_history_instance.study_history = f"{study_history_instance.study_history}\nReviewed on: {current_date}    |    " + "3 times Remember, now reset"
            study_history_instance.save()
            update_study_plan(memo_record)
            all_memo_records.remove(memo_record)

    print("--------------------------------------------------------------------------------> remember_count = " + str(remember_count))
    if remember_count in (0,1,2): 
            print("--------------------------------------------------------------------------------> timezone.now() = " + str(timezone.now()))
            memo_record.next_study_time = timezone.now() + timedelta(minutes=wait_time)
            print("--------------------------------------------------------------------------------> next_study_time = " + str(memo_record.next_study_time))
            memo_record.save()
    
    # print("--> now check history: remember_count  + " + str(remember_count))
    # print("======================================================> count for + " + str(remember_count))

    # else:
        
    #     if remember_count == 1: 
    #         wait_time = 1
    #     elif remember_count == 2: 
    #         wait_time = 2
    #     elif remember_count == 3: 
    #         wait_time = 3
    #     elif remember_count == 4: 
    #         wait_time = 4
    #     elif remember_count == 5: 
    #         print("--> now print count 5")
    #         current_date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    #         study_history_instance = memo_record.study_history_id
    #         study_history_instance.study_history = f"{study_history_instance.study_history}\nReviewed on: {current_date}    |    " + "5 times Remember, now reset"
    #         study_history_instance.save()
    #         update_study_plan(memo_record)
    #         all_memo_records.remove(memo_record)

    #     if remember_count in (1,2,3,4): 
    #            memo_record.next_study_time = timezone.now() + timedelta(minutes=wait_time)
    #            memo_record.save()


###########################################################################
########################################################################### classes 
########################################################################### 

class MemoRecordTop15(generics.ListAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        subject_type = self.request.GET.get('subject_type')

        if not subject_type:
            return MemoRecord.objects.none()

        return MemoRecord.objects.filter(
            author=user,
            subject_type=subject_type,
            current_learning_session=False,
            is_activate=True
        ).order_by('next_study_time')[:5]  ### Attention: This is 5 here - not 15. A temporary solution. 

class MemoRecordResetCurrentLearningSession(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        subject_type = request.data.get('subject_type')

        if not subject_type:
            return Response(
                {"error": "subject_type is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        # 更新 MemoRecord 记录
        try:
            updated_count = MemoRecord.objects.filter(
                subject_type=subject_type, author=user
            ).update(current_learning_session=False)
        except Exception as e:
            return Response(
                {"error": f"Failed to update records: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "message": f"Successfully reset {updated_count} records' current_learning_session to False.",
                "subject_type": subject_type,
                "updated_count": updated_count
            },
            status=status.HTTP_200_OK
        )

class BlogList(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author=user).order_by('-last_updated')
    
class SpecificBlog(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get("pk")
        return Blog.objects.filter(author=user, id=pk)    

class BlogCreate(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class BlogUpdate(generics.UpdateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
 
            instance = serializer.instance
            data = self.request.data

            for field, value in data.items():
                if hasattr(instance, field):  
                    setattr(instance, field, value)  
            
            instance.save()  
        else:
            print(serializer.errors)        

class BlogDelete(generics.DestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author=user)

class OneTimeEventDelete(generics.DestroyAPIView):
    serializer_class = OneTimeEventSerializer
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        user = self.request.user
        return OneTimeEvent.objects.filter(author=user)

class OneTimeEventList(generics.ListCreateAPIView):
    serializer_class = OneTimeEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return OneTimeEvent.objects.filter(author=user, is_done=False).order_by('start_date')

class OneTimeEventCreate(generics.ListCreateAPIView):
    serializer_class = OneTimeEventSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class OneTimeEventUpdate(generics.UpdateAPIView):
    serializer_class = OneTimeEventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return OneTimeEvent.objects.filter(author=user, is_done=False)

    def perform_update(self, serializer):
        if serializer.is_valid():
 
            instance = serializer.instance
            data = self.request.data

            for field, value in data.items():
                if hasattr(instance, field):  
                    setattr(instance, field, value)  
            
            instance.save()  
        else:
            print(serializer.errors)

class OneTimeEventDelete(generics.DestroyAPIView):
    serializer_class = OneTimeEventSerializer
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        user = self.request.user
        return OneTimeEvent.objects.filter(author=user)

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
 
    def get_queryset(self):
        user = self.request.user      

        memo_records = filter_by_next_study_time(user)
 
        memo_records = filter_by_study_scope(memo_records, user)
 
        memo_records = exam_every_record(memo_records)

        return get_seleted_50_memo_records(memo_records, 12)

class MemoRecordCreate(generics.ListCreateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        if serializer.is_valid():
 
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
        return SubjectType.objects.filter(author=user).order_by("type")

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
            
            remember_status = self.request.data.get('study_status', None)

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
    
class MemoRecordUpdate(generics.UpdateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            instance = serializer.instance
            data = self.request.data
            for field, value in data.items():
                # 确保该字段在模型中存在
                if hasattr(instance, field):
                    setattr(instance, field, value)  # 动态更新字段值
            # 保存更新后的实例
            instance.save()
            print(f"Updated MemoRecord: {instance.id}")
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
 
class StudyPlanReset(generics.UpdateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]
  
    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
 
            instance = serializer.instance
    
            study_plan_instance = instance.study_plan_id
             
            study_plan_instance.check_points = get_default_check_points()
 
            study_plan_instance.save() 

            print("Study plan reset successfully.")
        else:
            print(serializer.errors)

class MemoRecordSearch(generics.ListCreateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.GET.get('query', '')

        user = request.user
 
        memo_records = MemoRecord.objects.filter(
            Q(author=user) & (Q(question__icontains=search_query) | Q(record_details__icontains=search_query))
        )

        memo_records = memo_records.annotate(
            is_question_match=Case(
                When(question__icontains=search_query, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('-is_question_match')

        serializer = MemoRecordSerializer(memo_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
