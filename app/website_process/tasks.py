# from __future__ import absolute_import, unicode_literals
import requests
import uuid
import urllib
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urlparse
from celery import shared_task

from django.conf import settings
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import status

from common.const import WEBSITE_STATUSES
from .models import Website, WebsiteText, WebsiteImage


@shared_task
def website_process(url, website_id):
    try:
        website = Website.objects.get(pk=website_id)
        if website.status != WEBSITE_STATUSES.started:
            # log info that only website with status start is allowed to process
            # logger.debug("skip website_process because website was already processed")
            return
        website.status = WEBSITE_STATUSES.getting_text
        website.save(update_fields=["status"])
        content = requests.get(url, stream=True)
        soup = BeautifulSoup(content.text, 'html.parser')
        body = soup.find("body")
        [x.extract() for x in body.findAll('style')]
        [x.extract() for x in body.findAll('script')]
        text = body.get_text()
        WebsiteText.objects.create(website_id=website_id, text=text)

        parse_result = urlparse(url)
        imgs = body.findAll('img')
        website.images_count = len(imgs)
        website.save(update_fields=["images_count"])
        if len(imgs) == 0:
            website.status = WEBSITE_STATUSES.success
            website.save(update_fields=["status"])

        for img in body.findAll('img'):
            if img.has_attr("src"):
                img_url = urllib.parse.urljoin(
                    # parse_result.scheme + "://",
                    parse_result.hostname,
                    img.get("src")
                )
                image_process(img_url, website_id)

    except Exception as expt:
        # log expt
        website = get_object_or_404(Website, pk=website_id)
        website.status = WEBSITE_STATUSES.failed
        website.extra_context = str(expt)
        website.save(update_fields=["status", "extra_context"])


def get_image_from_response(response):
    # we need it to mock getting the image in unittests for better testing
    return Image.open(response.raw)


@shared_task
def image_process(url, website_id):
    try:
        _should_decrement_images_count = True
        website = get_object_or_404(Website, pk=website_id)
        response = requests.get(url, stream=True)
        if settings.SKIP_WRONG_URL_IMG_WEBSITE_PROCESSING \
                and not status.is_success(response.status_code):
            website.images_count = F('images_count') - 1
            website.save(update_fields=['images_count'])
            _should_decrement_images_count = False
        else:
            image = get_image_from_response(response)
            image_name = uuid.uuid4().hex + "." + str(image.format).lower()
            image_path = "/".join([settings.IMGS_DIR, image_name])
            # we can have thumbnail and resizing here if we want !!!
            image.save(image_path, image.format)
            WebsiteImage.objects.create(
                website_id=website_id,
                path_to_file=image_path
            )

        if website.images_count == WebsiteImage.objects.filter(website_id=website_id).count():
            website.status = WEBSITE_STATUSES.success
        elif WebsiteImage.objects.filter(website_id=website_id).count() >= 1 \
                and website.status != WEBSITE_STATUSES.getting_images:
            website.status = WEBSITE_STATUSES.getting_images
        website.save(update_fields=["status"])
    except Exception as expt:
        # log expt logger.error(expt)
        website = get_object_or_404(Website, pk=website_id)
        if not settings.SKIP_WRONG_URL_IMG_WEBSITE_PROCESSING:
            website.status = WEBSITE_STATUSES.failed
            website.extra_context = str(expt)
            website.save(update_fields=["status", "extra_context"])
        elif _should_decrement_images_count:
            if (website.images_count-1) == WebsiteImage.objects.filter(website_id=website_id).count():
                website.status = WEBSITE_STATUSES.success
            else:
                website.status = WEBSITE_STATUSES.getting_images

            website.images_count = F('images_count') - 1
            website.save(update_fields=['status', 'images_count'])
