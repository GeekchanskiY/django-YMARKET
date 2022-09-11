from django.db import models

# Create your models here.


class OfferCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    objects = models.Manager()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"


class Params(models.Model):
    name = models.TextField()
    value = models.TextField()
    related_category = models.ForeignKey(OfferCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"


class Offer(models.Model):
    name = models.TextField()
    picture = models.URLField()
    description = models.TextField()
    brand = models.TextField()
    category = models.ForeignKey(OfferCategory, on_delete=models.CASCADE)
    bar_code = models.IntegerField()
    params = models.TextField()
    price = models.FloatField()
    currency = models.CharField(default="RUB", max_length=6)
    vat = models.CharField(default="NO_VAT", max_length=15)
    home_url = models.URLField()
    min_quantity = models.IntegerField()
    step_quantity = models.IntegerField()
    dimensions = models.TextField()
    weight = models.TextField()
    disabled = models.BooleanField(default=True)
    amount = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return f"{str(self.name)} by {str(self.brand)}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
