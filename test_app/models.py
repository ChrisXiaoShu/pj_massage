from django.db import models
from datetime import datetime

class Customer(models.Model):
    line_id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    is_black = models.BooleanField(default=False)

    def __str__(self):
        return "{}_{}".format(self.name, self.phone)


class MasterGroup(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return "{}{}".format('group ', self.name)


class Master(models.Model):
    master_id = models.CharField(max_length=10, primary_key=True)
    group = models.ForeignKey(MasterGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    work_type = models.IntegerField(
        choices=[(1, '單'), (2, '雙')],
        default=1,
    )

    def __str__(self):
        return "{}_{}".format(self.group, self.name)


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, unique_for_date = 'datetime')
    datetime = models.DateTimeField(verbose_name="reservation_time")
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    has_remind = models.BooleanField(default=False)

    def __str__(self):
        return "{}_{}_{}_{}".format(self.id, self.master, datetime.strftime(self.datetime, '%Y%m%d%H%M'), self.name)