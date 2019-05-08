from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField


class PublicFields(models.Model):
    """
    we use those fields in other abstract models.
    """
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title')
    )
    image = FilerImageField(
        verbose_name=_('Image'),
        on_delete=models.CASCADE
    )
    text = RichTextUploadingField(
        verbose_name=_('Text')
    )

    class Meta:
        abstract = True
