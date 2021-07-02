from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Choices(models.Choices):
    YES = "yes"
    NO = "no"


class TestManyToMany(models.Model):
    """
    This model is being used to test many to many fields
    """

    pass


class TestOneToMany(models.Model):
    """
    This model is being used to test one to many fields
    """

    pass


class TestModel(models.Model):
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField()
    max_amount = models.IntegerField(validators=[MaxValueValidator(4)])
    min_amount = models.IntegerField(validators=[MinValueValidator(1)])
    choices = models.CharField(max_length=4, choices=Choices.choices)
    a_or_b = models.CharField(max_length=200, blank=True, validators=[RegexValidator(regex=r"(a|b)")])
    test_many = models.ManyToManyField(TestManyToMany, related_name="many_to_many")
    test_one = models.ForeignKey(TestOneToMany, related_name="one_to_many", on_delete=models.CASCADE)


class TestVerbosity(models.Model):
    text = models.TextField(null=True)
