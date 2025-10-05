from django.urls import path
from rest_framework.routers import DefaultRouter

from gym.views import (
    ProgramModelViewSet,
    ExerciseListCreateAPIView,
    ExerciseDetailAPIView,
)

router = DefaultRouter()

router.register(r"program", ProgramModelViewSet)

urlpatterns = [
    path(
        "exercises/",
        ExerciseListCreateAPIView.as_view({"get": "list", "post": "create"}),
        name="exercise-list",
    ),
    path(
        "exercises/<int:pk>",
        ExerciseDetailAPIView.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="exercise-detail",
    ),
]

urlpatterns += router.urls
