from django.shortcuts import render
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OfferCategorySerializer, OfferSerializer
from .models import OfferCategory, Offer, Params
from django.core.exceptions import ObjectDoesNotExist
import xml.etree.ElementTree as ET
import random
from datetime import datetime


# Create your views here.


class Import(APIView):
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        data = request.data

        try:
            category = OfferCategory.objects.get(name=data.get("category").lower())
        except ObjectDoesNotExist:
            try:
                category = Params.objects.get(name="Альтернативное имя", value=data.get("category").lower())\
                    .related_category
            except ObjectDoesNotExist:
                category = OfferCategory(name=data.get("category").lower())
                category.save()
        except:
            return Response({"err": "Error occurred. Probably there's no category arg"},
                            status=status.HTTP_400_BAD_REQUEST)
        data.pop("category")
        data.update({"category": category.id})
        serializer = OfferSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


class Update(APIView):
    def get(self, request, *args, **kwargs):
        per_day = Params.objects.get(name="Ultradar поиск в день").value
        offers = Offer.objects.all().order_by('modified')[0:int(per_day)]
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            category = OfferCategory.objects.get(name=data.get("category").lower())
        except:
            return Response({"err": "Error occurred. Probably there's wrong category arg"},
                            status=status.HTTP_400_BAD_REQUEST)

        offer = Offer.objects.get(category=category, name=data.get("name"))
        offer.price = data.get("price")
        offer.dimensions = data.get("dimensions")
        offer.weight = data.get("weight")
        offer.amount = data.get("amount")
        offer.params = data.get("detail_data")
        offer.disabled = False
        offer.save()
        return Response("Updated", status=status.HTTP_201_CREATED)


class YMLCreator:
    def __init__(self, data: list[Offer]):
        self.data: list[Offer] = data

    def create_yml(self):
        tree = ET.parse("template.xml")
        offers: list[Offer] = self.data
        root = tree.getroot()
        root.set("date", str(datetime.now()))
        offers_tag = root.find('shop').find('offers')
        categories_tag = root.find('shop').find('categories')
        all_categories = []
        for offer in offers:
            all_categories.append(offer.category)
        all_categories = list(set(all_categories))



class Export(APIView):
    def get(self, request, *args, **kwargs):
        categories = OfferCategory.objects.all()
        tree = ET.parse("template.xml")
        margin = int(Params.objects.get(name="Маржа").value)
        root = tree.getroot()
        root.set("date", str(datetime.now()))
        offers_tag = root.find('shop').find('offers')
        categories_tag = root.find('shop').find('categories')
        for category in categories:
            new_elem = ET.SubElement(categories_tag, "category", id=str(category.id))
            new_elem.text = category.name
            for offer in Offer.objects.filter(category=category):

                new_offer_elem = ET.SubElement(offers_tag, "offer", id=str(offer.SKU))
                offer_name = ET.SubElement(new_offer_elem, "name")
                offer_name.text = offer.name
                image = ET.SubElement(new_offer_elem, "picture")
                image.text = offer.picture
                description = ET.SubElement(new_offer_elem, "description")
                description.text = offer.description
                brand = ET.SubElement(new_offer_elem, "vendor")
                brand.text = offer.brand
                category_id = ET.SubElement(new_offer_elem, "categoryId")
                category_id.text = str(category.id)
                if offer.bar_code is not None or offer.bar_code == 1235234:
                    bar_code = ET.SubElement(new_offer_elem, "barcode")
                    bar_code.text = str(offer.bar_code)
                else:
                    bar_code = ET.SubElement(new_offer_elem, "barcode")
                    new_bar_code = 4000000000000 + random.randint(1000000000, 1000000000000)
                    offer.bar_code = new_bar_code
                    bar_code.text = str(new_bar_code)

                for param in offer.params.split(";"):
                    if len(param.split("|")) == 2:
                        param_el = ET.SubElement(new_offer_elem, "param", name=param.split("|")[0])
                        param_el.text = param.split("|")[1]
                    elif len(param.split("|")) == 3:
                        param_el = ET.SubElement(new_offer_elem, "param", name=param.split("|")[0],
                                                 unit=param.split("|")[2])
                        param_el.text = param.split("|")[1]
                price = ET.SubElement(new_offer_elem, "price")
                price.text = str(offer.price).replace(".", ",")
                old_price = ET.SubElement(new_offer_elem, "oldprice")
                old_price.text = str(offer.price + offer.price*margin/100).replace(".", ",")
                currency = ET.SubElement(new_offer_elem, "currencyId")
                currency.text = str(offer.currency)
                vat = ET.SubElement(new_offer_elem, "vat")
                vat.text = "NO_VAT"
                url = ET.SubElement(new_offer_elem, "url")
                url.text = str(offer.home_url)
                min_quantity = ET.SubElement(new_offer_elem, "min-quantity")
                min_quantity.text = str(offer.min_quantity)
                step_quantity = ET.SubElement(new_offer_elem, "step-quantity")
                step_quantity.text = str(offer.step_quantity)
                dimensions = ET.SubElement(new_offer_elem, "dimensions")
                dimensions.text = str(offer.dimensions)
                weight = ET.SubElement(new_offer_elem, "weight")
                weight.text = str(offer.weight)
                disabled = ET.SubElement(new_offer_elem, "disabled")
                if offer.disabled:
                    disabled.text = "true"
                else:
                    disabled.text = "false"

                count = ET.SubElement(new_offer_elem, "count")
                if not offer.disabled:
                    count.text = str(offer.amount)
                else:
                    count.text = str(0)
        with open("output.yml", "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)
        return FileResponse(open('output.yml', 'rb'))


        


