from django.db import models

class Type(models.Model):
    name = models.CharField(unique=True, blank=False, null=False, max_length=100)

class Item(models.Model):
    name = models.CharField(unique=True, blank=False, null=False, max_length=100)
    description = models.TextField(blank=True, null=False, max_length=250)
    quantity = models.PositiveIntegerField(blank=False, null=False )

    type = models.ForeignKey(
        Type, related_name="type", on_delete=models.CASCADE
    )