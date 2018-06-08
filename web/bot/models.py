from django.db import models


# Create your models here.
class Coffee(models.Model):
    name = models.CharField(max_length=30)
    size = models.IntegerField(default=1)
    syrup = models.IntegerField(default=1)
    cost = models.FloatField()

    def __str__(self):
        return self.name

class Size(models.Model):
    coffee_id = models.ForeignKey(Coffee, on_delete=None, related_name='+')
    size = models.IntegerField(default=0)
    cost = models.FloatField()


class Syrup(models.Model):
    name = models.CharField(max_length=30)
    cost = models.FloatField()
    emoji = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Orders(models.Model):
    user_id = models.IntegerField(default=0)
    coffee = models.ForeignKey(Coffee, on_delete=None)
    size = models.IntegerField(default=0)
    syrup = models.ForeignKey(Syrup, on_delete=None)
    cost = models.FloatField()
    ordered_at = models.DateTimeField("order's date")