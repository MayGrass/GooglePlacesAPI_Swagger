from rest_framework import serializers

LANGUAGE = serializers.CharField(
    required=False,
    help_text="See the [list of supported languages](https://developers.google.com/maps/faq#languagesupport).",
)
PRICE_RANGE = serializers.IntegerField(
    min_value=0,
    max_value=4,
    required=False,
    help_text="Valid values range between 0 (most affordable) to 4 (most expensive), inclusive.",
)


class GoogleAPIResponseFormatSerializer(serializers.Serializer):
    format = serializers.ChoiceField(["json", "xml"])


class FindPlaceSerializer(GoogleAPIResponseFormatSerializer):
    input = serializers.CharField(required=True)
    inputtype = serializers.ChoiceField(choices=["textquery", "phonenumber"], required=True)
    fields = serializers.ListField(
        required=False,
        help_text="[Place Data Fields](https://developers.google.com/maps/documentation/places/web-service/place-data-fields)",
    )
    language = LANGUAGE
    locationbias = serializers.ListField(
        required=False,
        help_text="[Prefer results in a specified area](https://developers.google.com/maps/documentation/places/web-service/search-find-place#locationbias)",
    )


class NearbySearchSerializer(GoogleAPIResponseFormatSerializer):
    location = serializers.CharField(help_text="This must be specified as `latitude,longitude`")
    radius = serializers.IntegerField(required=False, default=50000)
    keyword = serializers.CharField(required=False)
    language = LANGUAGE
    maxprice = PRICE_RANGE
    minprice = PRICE_RANGE
    name = serializers.CharField(required=False, help_text="Not Recommended")
    opennow = serializers.CharField(required=False)
    pagetoken = serializers.CharField(required=False)
    rankby = serializers.ChoiceField(["prominence", "distance"], required=False, default="prominence")
    type = serializers.CharField(
        required=False,
        help_text="See the list of [supported types](https://developers.google.com/maps/documentation/places/web-service/supported_types).",
    )


class TextSearchSerializer(NearbySearchSerializer):
    query = serializers.CharField()
    region = serializers.CharField(
        required=False,
        help_text="The region code, specified as a [ccTLD ('top-level domain')](https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains#Country_code_top-level_domains) two-character value.",
    )
    location = serializers.CharField(required=False, help_text="This must be specified as `latitude,longitude`")
    name = None
    rankby = None
    keyword = None
