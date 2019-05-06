from urllib.parse import urlparse
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .models import Website
from .serializers import WebsiteListSerializer, WebsiteCreateSerializer
from .tasks import website_process


class WebsiteList(generics.ListCreateAPIView, generics.RetrieveAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteListSerializer
    permission_classes = (AllowAny, )

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = WebsiteListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = WebsiteCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        website_url = serializer.validated_data['website_url']
        parse_result = urlparse(website_url)

        website = Website.objects.filter(
            hostname=parse_result.hostname,
            uri=parse_result.path
        )
        if not website.exists():
            website = Website.objects.create(
                hostname=parse_result.hostname,
                uri=parse_result.path
            )
            website_process(website_url, website.id)
        else:
            website = website.get()
        serializer = WebsiteListSerializer(website)
        return Response(serializer.data)


class WebsiteRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteListSerializer
