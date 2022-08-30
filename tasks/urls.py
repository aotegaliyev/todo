from django.urls import path

from tasks.views import TaskDetail, TaskList

urlpatterns = [
    path('api/v1/tasks', TaskList.as_view(), name='index'),
    path('api/v1/tasks/<int:pk>', TaskDetail.as_view(), name='detail'),
]
