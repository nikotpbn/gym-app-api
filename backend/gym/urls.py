from django.urls import path

from gym.views import (
    ProgramListCreateAPIView,
    ProgramDetailAPIView,
    ExerciseListCreateAPIView,
    ExerciseDetailAPIView,
)

urlpatterns = [
    path("programs/",
        ProgramListCreateAPIView.as_view({"get": "list", "post": "create"}),
        name="program-list",
    ),
    path("programs/<int:pk>",
        ProgramDetailAPIView.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="program-detail",
    ),
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
