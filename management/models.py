from django.db import models


#Курс доллара к гривне
class Dollar(models.Model):
    class Meta:
        db_table = 'dollar'
        verbose_name = 'Курс доллара'
        verbose_name_plural = 'Курсы доллара'

    dollar_to_hrn = models.FloatField(max_length=6, verbose_name='Курс', blank=False)
    dollar_date = models.DateTimeField(verbose_name='Дата установки курса', auto_now_add=True)
    dollar_active = models.BooleanField(verbose_name='Текущий курс', default=True)

# при обращении к классу Dollar возвращает его курс
    def __unicode__(self):
        return self.dollar_to_hrn


#Индекс повышения цены в гривне
class PriceIndex(models.Model):
    class Meta:
        db_table = 'priceIndex'
        verbose_name = 'Индекс повышения цены'
        verbose_name_plural = 'Индексы повышения цены'

    priceIndexValue = models.FloatField(max_length=6, verbose_name=' ', blank=False)
    priceIndex_fromStartPrice  = models.BooleanField(verbose_name='От начальной цены', default=False)
    priceIndex_date = models.DateTimeField(verbose_name='Дата установки индекса', auto_now_add=True)
    priceIndex_active = models.BooleanField(verbose_name='Текущий индекс', default=True)

# при обращении к классу Dollar возвращает его курс
    def __unicode__(self):
        return self.priceIndexValue