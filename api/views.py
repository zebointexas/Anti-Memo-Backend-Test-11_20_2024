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
from .models import Note, MemoRecord, OneTimeEvent
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
        return MemoRecord.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
           serializer.save(author=self.request.user)
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

    def perform_update(self, serializer):

        if serializer.is_valid():
        # 获取当前更新的实例（数据库中的原始值）
            instance = serializer.instance

            remember_status = self.request.headers.get('Remember-Status', 'default_status')

            print("remember_status = " + remember_status)

            # 获取数据库中原有的 memo_History 值
            memo_history = instance.memo_History or ''  # 防止 None 出现，默认空字符串
            
            # 获取当前时间
            current_date = localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')

            # 将新的更新时间追加到原有 memo_History
            updated_memo_history = f"{memo_history}\nReviewed on: {current_date}    |    {remember_status}"

            # 保存更新内容
            serializer.save(memo_History=updated_memo_history, author=self.request.user)
        else:
            print(serializer.errors)