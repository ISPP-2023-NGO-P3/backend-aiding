import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpeg', '.jpg', '.jfif', '.png', '.gif', '.bmp', '.dib', '.svg', '.svgz', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _('%(value)s  is unsupported file extension, the supported files extensions are: %(valid_extensions)s'))
