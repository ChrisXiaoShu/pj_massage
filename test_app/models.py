from django.db import models

class customer(models.Model):
    cName = models.CharField(max_length=10, null=False)
    cPhone = models.CharField(max_length=10, null=False)
    isBlack = models.BooleanField(default=False)
    def __str__(self):
        return "{}-{}".format(self.cName, self.cPhone)
