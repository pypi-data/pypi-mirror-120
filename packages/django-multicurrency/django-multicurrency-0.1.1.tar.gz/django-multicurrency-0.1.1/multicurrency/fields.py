from django.db import models

from .models import create_multicurrency_price_model, MulticurrencyPriceModel


class MultiCurrencyPriceField:
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        self.price_model = \
                create_multicurrency_price_model(cls, name, **self._kwargs)