from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("memo_records_list/", views.MemoRecordList.as_view(), name="memo-records-list"),
    path("memo_records/create/", views.MemoRecordCreate.as_view(), name="create-memo-record"),
    path("memo_records/delete/<int:pk>/", views.MemoRecordDelete.as_view(), name="delete-memo-record"),
    path("memo_records/update/study-history/<int:pk>/", views.MemoRecordUpdateStudyHistory.as_view(), name="update-memo-record-history"),
    path("memo_records/update/<int:pk>/", views.MemoRecordUpdate.as_view(), name="update-memo-record"),
    path("memo_records/search/", views.MemoRecordSearch.as_view(), name="search-memo-record"),
    path("subject_types_list/", views.SubjectTypeList.as_view(), name="subject-types-list"),
    path("subject_types/create/", views.SubjectTypeCreate.as_view(), name="create-subject-type"),
    path("subject_types/delete/<int:pk>/", views.SubjectTypeDelete.as_view(), name="delete-subject-type"),
    path("category_list/", views.SubjectTypeList.as_view(), name="subject-types-list"),
    path("study_scope/update/<int:pk>/", views.StudyScopeUpdate.as_view(), name="study-scope-update"),
    path("one_time_events_list/", views.OneTimeEventList.as_view(), name="fetch-one-time-events"),
    path("one_time_event/create/", views.OneTimeEventCreate.as_view(), name="create-one-time-event"),
    path("one_time_event/update/<int:pk>/", views.OneTimeEventUpdate.as_view(), name="update-one-time-event"),
    path("one_time_event/delete/<int:pk>/", views.OneTimeEventDelete.as_view(), name="delete-one-time-event"),

    path("blog_list/", views.BlogList.as_view(), name="fetch-blogs"),
    path("blog/<int:pk>/", views.SpecificBlog.as_view(), name="get-specific-blog"),
    path("blog/create/", views.BlogCreate.as_view(), name="create-blog"),
    path("blog/update/<int:pk>/", views.BlogUpdate.as_view(), name="update-blog"),
    path("blog/delete/<int:pk>/", views.BlogDelete.as_view(), name="delete-blog"),
]