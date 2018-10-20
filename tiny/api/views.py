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
import re
from api.utility import delete_http


class RecordList(APIView):
    def get(self, request, format=None):
        record = Record.objects.all()
        serializer = RecordSerializer(record, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            old_url = delete_http(request.data['old_url'])

            record = Record.objects.get(old_url=old_url)

            # 当前域名与tiny_url结合
            base = 'http://{0!s}/'.format(get_current_site(request).domain)
            record.tiny_url = urljoin(base, record.tiny_url)

            # 放入返回结果的serializer中
            tiny_url_serializer = TinyUrlSerializer(record)

            return Response(tiny_url_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def re(request, tiny_url):
    record = Record.objects.get(tiny_url=tiny_url)
    new_url = record.old_url
    # 统一加上入库时去掉的短网址
    new_url = "http://" + new_url
    return http.HttpResponsePermanentRedirect(new_url)



