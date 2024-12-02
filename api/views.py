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
            serializer.save(author=self.request.user)  # Optionally set the author to the current user
        else:
            print(serializer.errors)
 
 
        current_date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 获取现有的 memo_History 内容（如果有的话）
        memo_history = serializer.validated_data.get('memo_History', '')
        
        logging.error("memo_history = " + memo_history)

        # 追加当前日期到 memo_History 内容的末尾
        updated_memo_history = f"{memo_history}\nUpdated on: {current_date}"
        
        # 更新 memo_History 字段
        serializer.validated_data['memo_History'] = updated_memo_history
        
        # 保存更新的数据
        serializer.save(author=self.request.user)