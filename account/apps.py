from django.apps import AppConfig



class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        print("readyyyyy")

        import account.signals
