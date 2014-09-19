from django.db import models

CURRENCIES = ((1, 'BTC'), (2, 'LTC'))

class MetaDataPair(models.Model):
    key = models.TextField()
    value_str = models.TextField()
    value_numeric = models.FloatField(null=True)
    value_date = models.DateTimeField(null=True)
    item = models.ForeignKey('Alexandria.LibraryItem')
    
class LibraryItem(models.Model):
    hash = models.CharField(max_length=64)
    price_currency = models.IntegerField(choices=CURRENCIES)
    price_amount = models.FloatField(default=0)

    def set_metadata(self, metadata):
        for key, value in metadata:
            try:
                as_date = arrow.get(value).datetime
            except arrow.parser.ParserError:
                as_date = None
            
            try:
                as_number = float(vaue)
            except ValueError:
                as_number = None
            
            MetaDataPair.objects.create(
                value_str=value,
                value_date=as_date,
                value_numeric=as_number,
                key=key,
                item=self,
            )
            
class StorageEngine(models.Model):
    pass
