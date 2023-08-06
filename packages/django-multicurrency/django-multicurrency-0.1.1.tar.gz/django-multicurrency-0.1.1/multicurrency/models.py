from django.conf import settings
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
import sys

from .signals import price_pre_save_signal


CURRENCIES = [(currency_title.lower(), currency_title) 
               for currency_title in settings.MULTICURRENCY_CURRENCIES]


def create_multicurrency_price_model(shared_model, related_name, **kwargs):
    meta = {}
    capitalized_field_name = ''.join([ 
                            s.capitalize() for s in related_name.split('_') ])

    if shared_model._meta.abstract:
        raise TypeError("Can't create MulticurrencyPriceModel for " + 
                        "abstract class {0}".format(shared_model.__name__))

    meta['app_label'] = shared_model._meta.app_label
    meta['db_tablespace'] = shared_model._meta.db_tablespace
    meta['managed'] = shared_model._meta.managed
    meta.setdefault('db_table', f'{shared_model._meta.db_table}_{related_name}')
    meta.setdefault('default_permissions', ())

    name = str(f'{shared_model.__name__}{capitalized_field_name}')

    attrs = {}
    additional_params = ['verbose_name','blank','null']
    attrs['Meta'] = type(str('Meta'), (object,), meta)
    attrs['__module__'] = shared_model.__module__
    attrs['objects'] = models.Manager()
    _parent_relations_params={
        'to':shared_model, 
        'editable':False, 
        'on_delete':models.CASCADE,
        'related_name':related_name
    }
    for key, value in kwargs.items():
        if key not in additional_params:
            raise AttributeError(f"Unknown attribute {key}")
        _parent_relations_params[key] = value
    attrs['master'] = models.OneToOneField(**_parent_relations_params)

    # add columns for each currency
    for currency in settings.MULTICURRENCY_CURRENCIES:
        attrs[f'{currency.lower()}_amount'] = models.FloatField(
                                                    _('Amount'), 
                                                    blank=True, 
                                                    null=False)

    price_model = models.base.ModelBase(name, (MulticurrencyPriceModel,), attrs)

    mod = sys.modules[shared_model.__module__]
    setattr(mod, name, price_model)
    models.signals.pre_save.connect(price_pre_save_signal, price_model)

    return price_model


class MulticurrencyPriceModel(models.Model, metaclass=models.base.ModelBase):
    currency = models.CharField(_('Currency'),
                                max_length=3,
                                choices=CURRENCIES,
                                db_index=True)

    def __str__(self) -> str:
        title = f"{self.pk}"
        for currency in CURRENCIES:
            currency_price = getattr(self,f'{currency[0]}_amount')
            title += f" {currency[1]}({currency_price})"
        return title

    class Meta:
        abstract = True
        default_permissions = ()


class MulticurrencyPriceModelMixin(models.Model):
    def _fetch_price_field_model(self, field:str) -> MulticurrencyPriceModel:
        price_field = getattr(self._meta.model, field)
        if not isinstance(price_field, 
                models.fields.related_descriptors.ReverseOneToOneDescriptor):
            raise AttributeError(f"Price field must be a instance of " + 
                "models.fields.related_descriptors.ReverseOneToOneDescriptor")

        fields_list = self._meta.get_fields(include_hidden=True)
        for _field in fields_list:
            if _field.name == field: return _field.field.model
        raise AttributeError(f"No price field with title {field}")

    def _fetch_price_instance(self, field:str) -> MulticurrencyPriceModel:
        price_model = self._fetch_price_field_model(field)
        return price_model.objects.get(master=self)

    def create_price(self, field:str, currency:str, amount:float) -> \
                                                    MulticurrencyPriceModel:
        '''
            Create price related to parent
            Params:
                field - price field title
                currency - capitalized main currency from settings currency list
                amount - amount of price in main currency
            Result:
                Instance of recently created MulticurrencyPriceModel
        '''
        currency_field = f'{currency.lower()}_amount'
        price_model = self._fetch_price_field_model(field)

        return price_model.objects.create(**{
            'master':self,
            'currency':currency,
            currency_field:amount
        })

    def update_price(self, field:str, currency:str, amount:float) -> \
                                                    MulticurrencyPriceModel:
        '''
            Update price related to parent
            Params:
                field - price field title
                currency - capitalized main currency from settings currency list
                amount - amount of price in main currency
            Result:
                Instance of recently edited MulticurrencyPriceModel
        '''
        currency_field = f'{currency.lower()}_amount'
        price_instance = self._fetch_price_instance(field)
        price_instance.currency = currency
        setattr(price_instance,currency_field,amount)
        price_instance.save()

        return price_instance

    def delete_price(self, field:str) -> None:
        '''
            Delete price related to parent
            Params:
                field - price field title
            Result:
                None if success
        '''
        price_instance = self._fetch_price_instance(field)
        price_instance.delete()

    class Meta:
        abstract = True
        default_permissions = ()