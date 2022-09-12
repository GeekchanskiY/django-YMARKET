from rest_framework.serializers import HyperlinkedModelSerializer, SlugRelatedField
from .models import OfferCategory, Offer, Params


class OfferCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = OfferCategory
        fields = ('id', 'name')
        read_only_fields = ('id',)


class OfferSerializer(HyperlinkedModelSerializer):
    category = SlugRelatedField(
        queryset=OfferCategory.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Offer
        fields = ('id', 'name', 'picture', 'description', 'brand', 'category', 'bar_code', 'params', 'price',
                  'currency', 'vat', 'home_url', 'min_quantity', 'step_quantity', 'dimensions', 'weight', 'disabled',
                  'amount')
        read_only_fields = ('id',)
