from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TestModel(models.Model):
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField()
    max_amount = models.IntegerField(validators=[MaxValueValidator(4)])
    min_amount = models.IntegerField(validators=[MinValueValidator(1)])
