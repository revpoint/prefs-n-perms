from django.db import models


class Site(models.Model):
    def __unicode__(self):
        return u'Site {0}'.format(self.id)


class Customer(models.Model):
    site = models.ForeignKey('Site', related_name='customers')

    def __unicode__(self):
        return u'Customer {0} - Site {1}'.format(self.id, self.site.id)


class CustomerUser(models.Model):
    customer = models.ForeignKey('Customer', related_name='users')

    def __unicode__(self):
        return u'User {0} - Customer {1}'.format(self.id, self.customer.id)
