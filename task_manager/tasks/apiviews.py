from django.http.response import JsonResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView

from tasks.models import STATUS_CHOICES, Task

from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")



class TaskSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ["title", "description", "completed", "user."]

from rest_framework.permissions import IsAuthenticated


# class TaskViewSet(ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user, deleted=False)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class TaskListApi(APIView):

    def get(self, request):
        tasks = Task.objects.filter(deleted=True)
        data = TaskSerializer(tasks, many=True).data
        return Response({"tasks": data})


from django_filters.rest_framework import DjangoFilterBackend,FilterSet,CharFilter,ChoiceFilter

class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    # status = ChoiceFilter(choices=STATUS_CHOICES)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)