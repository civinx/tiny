from rest_framework import serializers
from api.models import Record
from django.contrib.sites.shortcuts import get_current_site
from api.utility import delete_http


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'tiny_url', 'old_url')

    def validate_old_url(self, value):
        # 当前域名
        domain = get_current_site(self.context['request']).domain
        old_url = delete_http(value)
        if old_url.startswith(domain):
            raise serializers.ValidationError("Cannot convert the url under the domain itself!")
        return value


class TinyUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('tiny_url', 'old_url')

