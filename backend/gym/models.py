from django.db import models
from django.utils.translation import gettext_lazy as _


class Exercise(models.Model):
    name = models.CharField(_("Exercise"), max_length=255)
    description = models.CharField(_("Description"), max_length=255)
    image = models.ImageField(upload_to="uploads", null=True, blank=True)


class Workout(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField(_("Sets"))
    reps = models.PositiveSmallIntegerField(_("Repetitions"))


class Training(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = "MON", _("Monday")
        TUESDAY = "TUE", _("Tuesday")
        WEDNESDAY = "WED", _("Wednesday")
        THURSDAY = "THU", _("Thursday")
        FRIDAY = "FRI", _("Friday")
        SATURDAY = "SAT", _("Saturday")

    pk = models.CompositePrimaryKey("day_of_week", "week_of_plan", "workout_id")
    day_of_week = models.CharField(
        _("Day of Week"),
        max_length=3,
        choices=DayOfWeek,
    )
    week_of_plan = models.PositiveSmallIntegerField(_("Week of Training Plan"))
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    superset_number = models.PositiveSmallIntegerField(null=True, blank=True)
