from django.db import models
from django.utils.translation import gettext_lazy as _


from django.contrib.auth import get_user_model

User = get_user_model()


class Program(models.Model):
    class ProgramType(models.TextChoices):
        POWER_BUILDING = "PBU", _("Power Building")
        BODY_BUILDING = "BBU", _("Body Building")
        POWER_LIFTING = "PLI", _("Power Lifting")
        FLEXIBILITY = "FLE", _("Flexibility")
        CALISTHENICS = "CAL", _("Calisthenics")

    users = models.ManyToManyField(User, through="Subscription")
    exercises = models.ManyToManyField("Exercise", through="ProgramExercise")
    name = models.CharField(_("Program Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    training_type = models.CharField(choices=ProgramType.choices, max_length=3)
    length_in_weeks = models.PositiveSmallIntegerField(_("Length in Weeks"))
    price = models.DecimalField(
        _("Price"), max_digits=10, decimal_places=2, default=0.00
    )
    currency = models.CharField(_("Currency"), max_length=3, default="USD")
    flat_discount = models.DecimalField(
        _("Flat Discount"),
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
    )
    percentage_discount = models.FloatField(
        _("Percentage Discount"), null=True, blank=True
    )


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    program = models.ForeignKey(Program, on_delete=models.RESTRICT)
    date_joined = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        _("Amount"), max_digits=10, decimal_places=2, default=0.00
    )
    currency = models.CharField(_("Currency"), max_length=3, default="USD")
    transaction_id = models.CharField(_("Transaction ID"), max_length=255)
    status = models.CharField(_("Status"), max_length=40)
    transaction_type = models.CharField(_("Transaction Type"), max_length=40)


class Exercise(models.Model):
    class AreaOfFocus(models.TextChoices):
        CHEST = "CHE", _("Chest")
        BACK = "BAC", _("Back")
        SHOULDERS = "SHO", _("Shoulders")
        BICEPS = "BIC", _("Biceps")
        TRICEPS = "TRI", _("Triceps")
        LEGS = "LEG", _("Legs")
        CORE = "COR", _("Core")

    name = models.CharField(_("Exercise"), max_length=255)
    area_of_focus = models.CharField(choices=AreaOfFocus)
    image = models.ImageField(upload_to="uploads", null=True, blank=True)


class ProgramExercise(models.Model):
    class EnvironmentChoices(models.TextChoices):
        HOME = "HO", _("Home")
        GYM = "GY", _("Gym")

    class DayOfWeekChoices(models.TextChoices):
        MONDAY = "MON", _("Monday")
        TUESDAY = "TUE", _("Tuesday")
        WEDNESDAY = "WED", _("Wednesday")
        THURSDAY = "THU", _("Thursday")
        FRIDAY = "FRI", _("Friday")
        SATURDAY = "SAT", _("Saturday")

    pk = models.CompositePrimaryKey(
        "day_of_week", "week_of_plan", "exercise_id", "program_id"
    )
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    program = models.ForeignKey("Program", on_delete=models.CASCADE)
    reps = models.PositiveSmallIntegerField(_("Exercise Repetitions"))
    sets = models.PositiveSmallIntegerField(_("Exercise Sets"))
    day_of_week = models.CharField(
        _("Day of Week"),
        max_length=3,
        choices=DayOfWeekChoices,
    )
    week_of_plan = models.PositiveSmallIntegerField(_("Week of Training Plan"))
    instructions = models.TextField(_("Instructions"), blank=True, null=True)
    instructions = models.TextField(_("Instructions"), blank=True, null=True)

    environment = models.CharField(
        _("Training Environment"),
        max_length=2,
        choices=EnvironmentChoices,
    )
    superset_number = models.PositiveSmallIntegerField(null=True, blank=True)
