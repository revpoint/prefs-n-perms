from prefs_n_perms import config, section_registry, model_registry
from test.test_app.models import Site, Customer, CustomerUser


class CustomerConfig(config.SectionConfig):
    tiers = ('site', 'customer', 'customer_user')
    default_preferences = {
        'theme': 'orange',
        'show_help_on_login': True,
    }
    available_permissions = (
        'can_invite_user',
        'can_disable_user',
        'can_access_billing',
        'can_reset_password',
    )

class SiteModelConfig(config.ModelConfig):
    model = Site

    def get_kwargs(self, obj):
        return {
            'site': obj.id,
        }

class CustomerModelConfig(config.ModelConfig):
    model = Customer

    def get_kwargs(self, obj):
        return {
            'site': obj.site.id,
            'customer': obj.id,
        }

class CustomerUserModelConfig(config.ModelConfig):
    model = CustomerUser

    def get_kwargs(self, obj):
        return {
            'site': obj.customer.site.id,
            'customer': obj.customer.id,
            'customer_user': obj.id,
        }


section_registry.register('customers', CustomerConfig)
model_registry.register('customers', 'site', SiteModelConfig)
model_registry.register('customers', 'customer', CustomerModelConfig)
model_registry.register('customers', 'customer_user', CustomerUserModelConfig)
