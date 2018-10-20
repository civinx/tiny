from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers import RecordSerializer, TinyUrlSerializer
from api.models import Record
from api.utility import gen
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django import http
from django.contrib.sites.shortcuts import get_current_site
from six.moves.urllib.parse import urljoin, urlsplit


class RecordList(APIView):
    def get(self, request, format=None):
        record = Record.objects.all()
        serializer = RecordSerializer(record, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            record = Record.objects.get(pk=serializer.data.get('id'))
            print(get_current_site(request).domain)
            base = 'http://{0!s}/'.format(get_current_site(request).domain)
            record.tiny_url = urljoin(base, record.tiny_url)
            tiny_url_serializer = TinyUrlSerializer(record)
            return Response(tiny_url_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def re(request, tiny_url):
    record = Record.objects.get(tiny_url=tiny_url)
    new_url = record.old_url
    if not new_url.startswith("http"):
        new_url = "https://" + new_url
    return http.HttpResponsePermanentRedirect(new_url)



