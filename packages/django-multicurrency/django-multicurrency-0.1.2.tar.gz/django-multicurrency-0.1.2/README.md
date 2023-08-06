# Django Multicurrency

Simple model multicurrency application for Django

## A brief overview

### Quick start

Installation via pip

```
pip install django-multicurrency
```

#### Add the following settings:

---

Install multicurrency app

```
INSTALLED_APPS += (
    'multicurrency',
)
```

Add currencies list and Exchange model to settings

```
MULTICURRENCY_CURRENCIES = ['UAH', 'EUR', 'USD']
MULTICURRENCY_EXCHANGER = 'shop.models.ExchangeRate'
```

### Creating models

---

#### Create Exchange model

Exchange model must contains staticmethod "`get_exchange_rate`", which must return exchange rate for two input currencies

```
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from multicurrency.models import CURRENCIES


class ExchangeRate(models.Model):
    currency_from = models.CharField(_('Currency'),
                                    max_length=3,
                                    choices=CURRENCIES,
                                    db_index=True,
                                    null=False)
    currency_to = models.CharField(_('Currency'),
                                    max_length=3,
                                    choices=CURRENCIES,
                                    db_index=True,
                                    null=False)
    exchange_rate = models.FloatField(_('Exchange rate'),
                                    null=False)
    created_at = models.DateTimeField(_('Created at'),
                                    blank=True,
                                    null=True,
                                    auto_now_add=True)

    @staticmethod
    def get_exchange_rate(currency_from:str, currency_to:str):
        try:
            return ExchangeRate.objects.filter(
                currency_from=currency_from.lower(),
                currency_to=currency_to.lower()
            ).latest('created_at').exchange_rate
        except ExchangeRate.DoesNotExist:
            return None

    def __str__(self) -> str:
        return f"{self.get_currency_from_display()} -> " + \
               f"{self.get_currency_to_display()} {self.exchange_rate}"
```

#### Create Price model

```
from django.db import models

from multicurrency.fields import MultiCurrencyPriceField
from multicurrency.models import MulticurrencyPriceModelMixin

class Product(MulticurrencyPriceModelMixin):
    title = models.CharField()
    price = MultiCurrencyPriceField(verbose_name="Product price")
```

MultiCurrencyPriceField accept as kwargs:

* verbose_name
* null
* blank

### Accessing fields

MultiCurrencyPriceField has 3 methods to access price fields:

* PriceModel.create_<price_field_title>(price_field_title, currency, amount)
* PriceModel.update_<price_field_title>(price_field_title, currency, amount)
* PriceModel.delete_<price_field_title>(price_field_title)

```
>>> from shop.models import Product
>>> product = Product.objects.create(title='Jeans')
>>> product.create_price('price','USD',10)
<ProductPrice: EUR(11.7) USD(10)>
>>> product.update_price('price','USD',20)
<ProductPrice: EUR(23.4) USD(20)>
>>> product.delete_price('price')
None
```
