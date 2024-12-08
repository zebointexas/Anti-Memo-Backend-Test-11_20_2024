from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("memo_records/", views.MemoRecordListCreate.as_view(), name="memo-records-list"),
    path("memo_records/delete/<int:pk>/", views.MemoRecordDelete.as_view(), name="delete-memo-record"),
    path("memo_records/update/<int:pk>/", views.MemoRecordUpdate.as_view(), name="update-memo-record"),
]