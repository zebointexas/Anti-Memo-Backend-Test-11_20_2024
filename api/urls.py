from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("memo_records_list/", views.MemoRecordList.as_view(), name="memo-records-list"),
    path("memo_records/create/", views.MemoRecordCreate.as_view(), name="create-memo-record"),
    path("memo_records/delete/<int:pk>/", views.MemoRecordDelete.as_view(), name="delete-memo-record"),
    path("memo_records/update/study-history/<int:pk>/", views.MemoRecordUpdateStudyHistory.as_view(), name="update-memo-record"),
    path("memo_records/update/record-details/<int:pk>/", views.MemoRecordUpdateRecordDetails.as_view(), name="update-record-details"),
    path("subject_types_list/", views.SubjectTypeList.as_view(), name="subject-types-list"),
    path("subject_types/create/", views.SubjectTypeCreate.as_view(), name="create-subject-type"),
    path("subject_types/delete/<int:pk>/", views.SubjectTypeDelete.as_view(), name="delete-subject-type"),
    path("category_list/", views.SubjectTypeList.as_view(), name="subject-types-list"),
    path("study_scope/update/<int:pk>/", views.StudyScopeUpdate.as_view(), name="study-scope-update"),
]