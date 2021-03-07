from io import BytesIO
from scour import scour

from django.db.models import FileField
from django.core.validators import ValidationError
from django.utils.translation import ugettext_lazy as _


class SVGField(FileField):
    def validate(self, value, model_instance):
        if b"http://www.w3.org/2000/svg" not in value.read():
            raise ValidationError(_("Le fichier n'est pas un SVG."))
        value.seek(0)
        return super().validate(value, model_instance)

    def clean(self, value, model_instance):
        cleaned_value = super().clean(value, model_instance)
        content = cleaned_value.read()
        scour_options = scour.sanitizeOptions(options=None)
        scour_options.remove_metadata = True
        clean_svg = scour.scourString(content, options=scour_options)
        cleaned_value.file.file = BytesIO(clean_svg.encode())
        return cleaned_value
