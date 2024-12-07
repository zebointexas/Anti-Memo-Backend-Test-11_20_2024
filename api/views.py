import logging
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    UserSerializer,
    NoteSerializer,
    MemoRecordSerializer,
    OneTimeEventSerializer,
)
from .models import Note, MemoRecord, OneTimeEvent, StudyHistory, StudyPlan, get_default_study_check_points
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import localtime, now
from datetime import timedelta


# Note List and Create View
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
####################################################################################
####################################################################################
####################################################################################



# MemoRecord List and Create View
class MemoRecordListCreate(generics.ListCreateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]
 
    def get_last_word(self, eachLine):
        words = eachLine.strip().split()
        if not words:
            return None
        return words[-1]

    def update_study_plan(self, record, last_five_lines, memo_records):
        update_study_check_points = True
    
        if not last_five_lines: 
           update_study_check_points = False 

        for eachLine in last_five_lines:
            if not eachLine.strip(): 
                update_study_check_points = False
            last_word = self.get_last_word(eachLine)
            if last_word == 'Forget':
                update_study_check_points = False

        if update_study_check_points:
            study_check_points = record.study_plan.study_check_points
            for key, value in study_check_points.items():
                if value == "false":
                    study_check_points[key] = "true"
                    record.study_plan.study_check_points = study_check_points
                    record.study_plan.save()
                    memo_records.remove(record)  
                    print("------------------------------------------------------------ memo_records deleted in update_study_plan"); 


    def check_study_history(self, record, last_five_lines, last_updated_time, memo_records):
        remove_this_record = True; 
        
        remember_count = 0; 

        if not last_five_lines: 
            remove_this_record = False

        for eachLine in reversed(last_five_lines):
            print("------------------------------------------------------------ eachLine = " + eachLine)
            if eachLine.strip():                 
                last_word = self.get_last_word(eachLine)
                if last_word == 'Remember':
                   remember_count += 1
                if last_word == 'Forget':
                    break

        time_difference = int( (timezone.now() - last_updated_time).total_seconds() / 60 )

        # print("------------------------------------------------------------ time_difference = " + str(time_difference) )
        # print("------------------------------------------------------------ remember_count = " + str(remember_count))
        if( ( remember_count == 1 and time_difference > 5)   or 
            ( remember_count == 2 and time_difference > 15)  or
            ( remember_count == 3 and time_difference > 35)  or
            ( remember_count == 4 and time_difference > 75)  or
            ( remember_count == 5 and time_difference > 115) 
        ):
            remove_this_record = False
            print("------------------------------------------------------------ checked and true")

        if remember_count == 0: 
           remove_this_record = False

        if remove_this_record: 
            memo_records.remove(record)  
            print("------------------------------------------------------------ memo_records deleted in check_study_history"); 
            
    def get_queryset(self):
        user = self.request.user
        memo_records = MemoRecord.objects.filter(author=user).select_related('study_plan', 'study_history')
        memo_records = list(memo_records)             

        print("------------------------------------------------------------ total records " + str(len(memo_records))); 
 
        for record in memo_records[:]:
            if record.study_history: 
                study_history_content = record.study_history.study_history   
                last_updated_time = record.study_history.last_updated
                study_history_lines = study_history_content.splitlines()
                last_five_lines = study_history_lines[-5:]  
                self.update_study_plan(record, last_five_lines, memo_records)
                self.check_study_history(record, last_five_lines, last_updated_time, memo_records)
        return memo_records
    
   
    def perform_create(self, serializer):
        if serializer.is_valid():
 
            study_plan = StudyPlan.objects.create(
                nominal_start_date_for_progress_calculation=timezone.now(),
                study_check_points=get_default_study_check_points()
            )
 
            study_history = StudyHistory.objects.create(
                study_history="Initial Study History",
                study_days_count="1",
                record_details_change_history="Initial History Details"
            )
 
            memo_record = serializer.save(author=self.request.user, study_plan=study_plan, study_history=study_history);
        else:
            print(serializer.errors)

class MemoRecordDelete(generics.DestroyAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)
 
class MemoRecordUpdate(generics.UpdateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)
 
    # def perform_update(self, serializer):
    #     if serializer.is_valid():
 
    #         instance = serializer.instance
 
    #         study_history_instance = instance.study_history
 
    #         if study_history_instance:
    #             study_history = study_history_instance.study_history
    #         else:
    #             study_history = ''
 
    #         remember_status = self.request.headers.get('Remember-Status', 'default_status')
    #         print("remember_status = " + remember_status)
 
    #         current_date = localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
 
    #         updated_study_history = f"{study_history}\nReviewed on: {current_date}    |    {remember_status}"
 
    #         study_history_instance.study_history = updated_study_history
    #         study_history_instance.save()  
 
    #         serializer.save(author=self.request.user)
    #         print("Study history updated successfully.")
    #     else:
    #         print(serializer.errors)

    def perform_update(self, serializer):
        if serializer.is_valid():
            instance = serializer.instance
            memo_record_id = self.kwargs.get('pk')
            memo_record = MemoRecord.objects.filter(id=memo_record_id)

            remember_status = self.request.headers.get('Remember-Status', 'default_status')
            current_date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

            study_history_instance = instance.study_history
            
            if study_history_instance:
                study_history = study_history_instance.study_history
            else:
                study_history = ''

            updated_study_history = f"{study_history}\nReviewed on: {current_date}    |    {remember_status}"
            memo_record.study_history = updated_study_history

            study_history_instance.study_history = updated_study_history
            study_history_instance.save()  

            serializer.save(author=self.request.user)
            print("Study history updated successfully.")
        else:
            print(serializer.errors)