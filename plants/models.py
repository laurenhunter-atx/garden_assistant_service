from django.db import models
from accounts.models import User


class Plant(models.Model):
    name = models.CharField(max_length=100)
    plant_date = models.DateField(auto_now=True)
    days_to_harvest = models.PositiveSmallIntegerField(default=0)
    owner = models.ForeignKey(User, related_name="plants", on_delete=models.CASCADE, null=True)
