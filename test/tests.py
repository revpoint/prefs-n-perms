from django.test import TestCase
from test.test_app.models import Site, Customer, CustomerUser


class TestSections(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()

class TestPreferences(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.site = Site.objects.create()
        self.customer = Customer.objects.create(site=self.site)
        self.customer_user = CustomerUser.objects.create(customer=self.customer)

    def test_default_preferences(self):
        self.assertEqual(self.site.preferences, self.customer.preferences)
        self.assertEqual(self.site.preferences, self.customer_user.preferences)

class TestPermissions(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
