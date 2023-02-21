from django.db import models


class TypedUrls(models.Model):
    entered_url = models.URLField("Entered Url", null=True)
    returned_url = models.URLField("Returned Url", null=True)
    dates = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.entered_url)

    class Meta:
        verbose_name_plural = "Typed Urls"
