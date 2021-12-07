from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import requests
from google_places_api_swagger.api.serializers import *
from django.conf import settings
from rest_framework.request import Request

API_KEY = settings.GOOGLE_API_KEY or None

BASE_URL = "https://maps.googleapis.com/maps/api/place/"

FIND_PLACE_URL = BASE_URL + "findplacefromtext/"

NEARBY_SEARCH_URL = BASE_URL + "nearbysearch/"

TEXT_SEARCH_URL = BASE_URL + "textsearch/"


def request_api(serialzier_class: serializers.Serializer, request: Request, request_url: str) -> dict:
    serializer = serialzier_class(data=request.GET)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data

        # reponse格式選擇 json, xml
        output_format = data["format"]
        del data["format"]
        request_url += output_format

        data["key"] = request.GET.get("key") or API_KEY
        response = requests.get(request_url, params=data)
        print(response.url)
        return response.json() if output_format == "json" else response.text


class FindPlace(ViewSet):
    @swagger_auto_schema(
        query_serializer=FindPlaceSerializer,
        operation_id="Find Place",
        operation_description="https://developers.google.com/maps/documentation/places/web-service/search-find-place",
        tags=["Place Search"],
    )
    @action(detail=False)
    def findplacefromtext(self, request):
        return Response(request_api(FindPlaceSerializer, request, FIND_PLACE_URL))

    @swagger_auto_schema(
        query_serializer=NearbySearchSerializer,
        operation_id="Nearby Search",
        operation_description="https://developers.google.com/maps/documentation/places/web-service/search-nearby",
        tags=["Place Search"],
    )
    @action(detail=False)
    def nearbysearch(self, request):
        return Response(request_api(NearbySearchSerializer, request, NEARBY_SEARCH_URL))

    @swagger_auto_schema(
        query_serializer=TextSearchSerializer,
        operation_id="Text Search",
        operation_description="https://developers.google.com/maps/documentation/places/web-service/search-text",
        tags=["Place Search"],
    )
    @action(detail=False)
    def textsearch(self, request):
        return Response(request_api(TextSearchSerializer, request, TEXT_SEARCH_URL))
