from django.contrib import admin
from .models import Program, Exercise, ProgramExercise

# Register your models here.
admin.site.register(Program)
admin.site.register(Exercise)
admin.site.register(ProgramExercise)
