from django.conf import settings

from .exceptions import MulticurrencyException
from .utils import import_class


def price_pre_save_signal(sender, instance, raw, **kwargs):
    Exchanger = import_class(settings.MULTICURRENCY_EXCHANGER)
    if not hasattr(Exchanger, 'get_exchange_rate'):
        raise MulticurrencyException(f'Please provide "get_exchange_rate" method for exchanger {Exchanger}')

    main_currency = instance.currency
    amount = getattr(instance, f'{main_currency.lower()}_amount', None)

    if not amount:
        raise MulticurrencyException(f'Please, provide amount in {main_currency}')

    exchanger = Exchanger()

    currencies_list = list(settings.MULTICURRENCY_CURRENCIES)
    currencies_list.remove(main_currency.upper())

    for currency in currencies_list:

        exchange_rate = exchanger.get_exchange_rate(main_currency.lower(), 
                                                        currency.lower())
        if not exchange_rate:   
            exchange_rate = exchanger.get_exchange_rate(currency.lower(), 
                                                        main_currency.lower()) 
            if not exchange_rate:
                raise MulticurrencyException(
            f'No exchange rate for pair {main_currency.upper()}/{currency} or {currency}/{main_currency.upper()}')
            
            exchange_rate = 1/exchange_rate

        setattr(instance, f'{currency.lower()}_amount', amount*exchange_rate)