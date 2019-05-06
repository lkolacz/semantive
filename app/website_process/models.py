from django.db import models
from common.const import WEBSITE_STATUSES


class Website(models.Model):
    hostname = models.CharField(max_length=255)
    uri = models.CharField(max_length=255)
    status = models.CharField(max_length=3, choices=WEBSITE_STATUSES, default=WEBSITE_STATUSES.started)
    images_count = models.PositiveIntegerField(default=0)
    extra_context = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return f"{self.__class__.__name__.lower()} no: <{self.pk}> {self.hostname} {self.uri}"

    def get_status(self):
        return self.status and WEBSITE_STATUSES[self.status]


class WebsiteText(models.Model):
    website = models.OneToOneField("Website", on_delete=models.deletion.CASCADE, related_name="text")
    text = models.TextField()

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return f"{self.__class__.__name__} no: <{self.pk}> {self.website.hostname} {self.website.uri}"


class WebsiteImage(models.Model):
    website = models.ForeignKey(Website, on_delete=models.deletion.CASCADE, related_name="images")
    path_to_file = models.CharField(max_length=255)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return f"{self.__class__.__name__} no:  <{self.pk}> {self.website.hostname} {self.website.uri}"
