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
class MemoRecordRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = MemoRecord.objects.all()
    serializer_class = MemoRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MemoRecord.objects.filter(author=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)  # Update the author to the current user (optional)
        else:
            print(serializer.errors)
 