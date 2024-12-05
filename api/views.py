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


# Note Delete View
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
 
    def get_queryset(self):
        user = self.request.user
        memo_records = MemoRecord.objects.filter(author=user).select_related('study_plan', 'study_history')

        for record in memo_records:
            if record.study_history:
                study_history_content = record.study_history   
                # study_history_lines = study_history_content.
                # last_five_lines = study_history_lines[-5:]

        return memo_records
    
    def perform_create(self, serializer):
        if serializer.is_valid():

            print("Test Step 1 ------");

            study_plan = StudyPlan.objects.create(
                nominal_start_date_for_progress_calculation=timezone.now(),
                study_check_points=get_default_study_check_points()
            )

            print("Test Step 2 ------");

            study_history = StudyHistory.objects.create(
                study_history="Initial Study History",
                today_study_count="1",
                record_details_change_history="Initial History Details"
            )

            print("Test Step 3 ------");

            memo_record = serializer.save(author=self.request.user, study_plan=study_plan, study_history=study_history);
        
            print("Test Step 4 ------");

        else:
            print(serializer.errors)
class MemoRecordDelete(generics.DestroyAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)

# MemoRecord Retrieve, Update, Delete View
class MemoRecordUpdate(generics.UpdateAPIView):
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)

    # def perform_update(self, serializer):

    #     if serializer.is_valid():

    #         instance = serializer.instance

    #         remember_status = self.request.headers.get('Remember-Status', 'default_status')

    #         print("remember_status = " + remember_status)

    #         # 获取数据库中原有的 memo_History 值
    #         study_history = instance.study_history or ''  # 防止 None 出现，默认空字符串
            
    #         # 获取当前时间
    #         current_date = localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')

    #         # 将新的更新时间追加到原有 memo_History
    #         updated_study_history = f"{study_history}\nReviewed on: {current_date}    |    {remember_status}"

    #         # 保存更新内容
    #         serializer.save(study_history=updated_study_history, author=self.request.user)
    #     else:
    #         print(serializer.errors)

    def perform_update(self, serializer):
        if serializer.is_valid():
            # 获取当前更新的实例（即 MemoRecord 实例）
            instance = serializer.instance

            # 获取通过 memo_record 关联的 study_history 外键实例
            study_history_instance = instance.study_history

            # 如果 study_history 实例存在，获取其中的内容，否则使用空字符串
            if study_history_instance:
                study_history = study_history_instance.study_history
            else:
                study_history = ''

            # 从请求头中获取 'Remember-Status'，如果没有则使用 'default_status'
            remember_status = self.request.headers.get('Remember-Status', 'default_status')
            print("remember_status = " + remember_status)

            # 获取当前时间
            current_date = localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')

            # 将新的更新时间和状态信息追加到原有 study_history
            updated_study_history = f"{study_history}\nReviewed on: {current_date}    |    {remember_status}"

            # 更新 StudyHistory 实例的 study_history 字段
            study_history_instance.study_history = updated_study_history
            study_history_instance.save()  # 保存更新后的 StudyHistory

            # 最后保存 MemoRecord 内容，保持外键关系不变
            serializer.save(author=self.request.user)
            print("Study history updated successfully.")
        else:
            print(serializer.errors)