from __future__ import unicode_literals

from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from numbers import Number

# Create your models here.
class CustomerManager(models.Manager):
    def validation(self, **kwargs):
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        iban = kwargs['iban']
        administrator = kwargs['administrator']
        errors = {}

        if first_name == '':
            errors['name'] = 'First Name should not be empty .'

        if last_name == '':
            errors['last_name'] = 'Last Name should not be empty.'

        if iban == '' or len(iban) < 20 or (not iban.isdigit()):
            errors['iban'] = 'IBAN should not be empty and must have at least 20 numbers.'

        if errors:
            return(False, errors)
        else:
            return(True, '')

    def create(self, **kwargs):
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        iban = kwargs['iban']
        administrator = kwargs['administrator']
        validation = self.validation(first_name=first_name, last_name=last_name, iban=iban, administrator=administrator)
        if not validation[0]:
            return(False, validation[1])
        else:
            customer = Customer(first_name=first_name, last_name=last_name, iban=iban, administrator=administrator)
            customer.save()
            return(True, administrator.id)

    def remove(self, administrator, customer):
        try:
            customer = self.get(id=customer, administrator__id=administrator)

            customer.delete()
        except Exception as e:
            pass

    def update(self, **kwargs):
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        iban = kwargs['iban']
        administrator = kwargs['administrator']
        customer = kwargs['customer']
        validation = self.validation(first_name=first_name, last_name=last_name, iban=iban, administrator=administrator)
        print(validation[0])

        if not validation[0]:
            return(False, validation[1])
        else:
            print('qitu jom')
            try:
                customer_update = self.filter(id=customer, administrator=administrator)
                customer_update.update(first_name=first_name, last_name=last_name, iban=iban)
            except Exception as e:
                raise
            return(True, administrator)


class Customer(models.Model):
    first_name = models.CharField(max_length=45, blank=True)
    last_name = models.CharField(max_length=45, blank=True)
    iban = models.CharField(max_length=250, blank=True)
    administrator = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = CustomerManager()


    class Meta:
        db_table = 'app_customers'
