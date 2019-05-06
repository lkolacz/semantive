from rest_framework import serializers
from .models import Website, WebsiteText, WebsiteImage


class WebsiteTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebsiteText
        fields = "__all__"


class WebsiteImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebsiteImage
        fields = "__all__"


class WebsiteListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status', read_only=True)
    text = WebsiteTextSerializer()
    images = WebsiteImageSerializer(many=True)

    class Meta:
        model = Website
        fields = "__all__"


class WebsiteCreateSerializer(serializers.Serializer):
    website_url = serializers.URLField()
