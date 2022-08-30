from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.decorators import allowed_users, user_can_update_or_delete

from tasks.models import Task
from tasks.serializers import TaskSerializer, TaskUpdateSerializer


@method_decorator(allowed_users(['employee']), name='post')
class TaskList(APIView):
    def get(self, request, format=None):
        tasks = Task.objects.all().order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['author'] = request.user.id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # send_date = task.deadline - timedelta(hours=1)
            # send_async_notification.apply_async((task), eta=send_date)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(allowed_users(['employee', 'admin']), name='put')
@method_decorator(user_can_update_or_delete, name='put')
@method_decorator(allowed_users(['employee', 'admin']), name='delete')
@method_decorator(user_can_update_or_delete, name='delete')
class TaskDetail(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
