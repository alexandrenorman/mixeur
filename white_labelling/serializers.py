import serpy

from helpers.serializers import AutoModelSerializer

from white_labelling.helpers import wl_cdn
from white_labelling.models import WhiteLabelling


class WhiteLabellingSerializer(AutoModelSerializer):
    model = WhiteLabelling
    exclude = ["smtp_account", "sms_account"]

    neutral_domain_for_newsletters = serpy.MethodField()

    def get_header(self, obj):
        return wl_cdn.header(obj)

    def get_footer(self, obj):
        return wl_cdn.footer(obj)

    def get_style(self, obj):
        return wl_cdn.style(obj)

    def get_json(self, obj):
        return wl_cdn.get_data(obj)

    def get_neutral_domain_for_newsletters(self, obj):
        try:
            neutral = WhiteLabelling.objects.get(is_neutral_for_newsletters=True)
        except WhiteLabelling.DoesNotExist:
            neutral = obj

        return neutral.domain
