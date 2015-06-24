import logging
from django.test import TestCase
from test.test_app.models import Site, Customer, CustomerUser


class TestSections(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.site_1 = Site.objects.create()
        self.customer_1 = Customer.objects.create(site=self.site_1)
        self.customer_user_1 = CustomerUser.objects.create(customer=self.customer_1)
        self.customer_2 = Customer.objects.create(site=self.site_1)
        self.customer_user_2 = CustomerUser.objects.create(customer=self.customer_2)
        self.site_2 = Site.objects.create()
        self.customer_3 = Customer.objects.create(site=self.site_2)
        self.customer_user_3 = CustomerUser.objects.create(customer=self.customer_3)
        self.customer_user_4 = CustomerUser.objects.create(customer=self.customer_3)

    def test_site(self):
        self.assertEqual(self.site_1.id, 1)
        logging.info(dir(self.site_1))

class TestPreferences(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()

class TestPermissions(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
