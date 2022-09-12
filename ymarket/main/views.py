from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OfferCategorySerializer, OfferSerializer
from .models import OfferCategory, Offer, Params
from django.core.exceptions import ObjectDoesNotExist


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
    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            category = OfferCategory.objects.get(name=data.get("category").lower())
        except:
            return Response({"err": "Error occurred. Probably there's wrong category arg"},
                            status=status.HTTP_400_BAD_REQUEST)

        offer = Offer.objects.get(category=category, name=data.get("name"))
        return Response({"a": 1}, status=status.HTTP_201_CREATED)


