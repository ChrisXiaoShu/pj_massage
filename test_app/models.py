from django.db import models

class Customer(models.Model):
    line_id = models.CharField()
    c_name = models.CharField(max_length=10, null=False)
    c_phone = models.CharField(max_length=10, null=False)
    is_black = models.BooleanField(default=False)

    def __str__(self):
        return "{}_{}".format(self.cName, self.cPhone)


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField()
    c_name = models.CharField(max_length=10, null=False)
    c_phone = models.CharField(max_length=10, null=False)
