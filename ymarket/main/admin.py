from django.contrib import admin
from .models import Offer, OfferCategory, Params
# Register your models here.


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'amount')
    search_fields = ('name',)
    list_filter = ('modified', 'disabled')
    
    fields = ('name', 'picture', 'description', 'brand', 'category', 'bar_code', 'params', 'price',
              'currency', 'vat', 'home_url', 'min_quantity', 'step_quantity', 'dimensions', 'weight', 'disabled',
              'amount', 'modified', 'created')
    readonly_fields = ('created',)


@admin.register(OfferCategory)
class OfferCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ymarket_id')
    search_fields = ('name', 'ymarket_id')
    fields = ('name', 'ymarket_id')


@admin.register(Params)
class ParamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'related_category')
    search_fields = ('name', )
    fields = ('name', 'value', 'related_category')

