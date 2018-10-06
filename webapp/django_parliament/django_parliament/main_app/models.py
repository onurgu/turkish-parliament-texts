from django.db import models

# Create your models here.

class Dummy(models.Model):
    field1 = models.TextField()
    field2 = models.IntegerField()

    def __str__(self):
        return self.field1