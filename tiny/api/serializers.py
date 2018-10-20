from rest_framework import serializers
from api.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'tiny_url', 'old_url')


class TinyUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('tiny_url',)

