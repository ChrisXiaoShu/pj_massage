from django.db import models

class Customer(models.Model):
    line_id = models.CharField(max_length=30, null=False)
    c_name = models.CharField(max_length=10, null=False)
    c_phone = models.CharField(max_length=10, null=False)
    is_black = models.BooleanField(default=False)

    def __str__(self):
        return "{}_{}".format(self.c_name, self.c_phone)


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField()
    c_name = models.CharField(max_length=10, null=False)
    c_phone = models.CharField(max_length=10, null=False)

@classmethod
def make_reservation(reservation, massager, date, customer, c_name, c_phone):
    status = False
    # with transaction.atomic():
    #     q_reservation = (
    #        reservation.objects
    #        .select_for_update()
    #        .get(customer = customer, massager = massager, date = date)
    #     )

    #     if not q_reservation:
    #         reservation.objects.create()
    #         status = True
    obj, created = Person.objects.get_or_create(
    first_name='John',
    last_name='Lennon',
    defaults={'birthday': date(1940, 10, 9)},
)   
          
    return status

class MassagerGroup(models.Model):
    g_name = models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{}{}".format('massage group ', self.g_name)

class Massager(models.Model):
    massagergroup = models.ForeignKey(MassagerGroup, on_delete=models.CASCADE)
    m_name = models.CharField(max_length=10, null=False)