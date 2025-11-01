# -*- coding: utf-8 -*-
"""
Data API Serializers
"""

from rest_framework import serializers
from apps.data.domain.models import UnifiedDataItem


class UnifiedDataItemSerializer(serializers.Serializer):
    """UnifiedDataItem 직렬화"""
    id = serializers.IntegerField()
    type = serializers.CharField(source='data_type.value')
    date = serializers.DateField()
    title = serializers.CharField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    category = serializers.CharField(allow_null=True)
    description = serializers.CharField(allow_null=True)
    uploaded_at = serializers.DateTimeField()
    uploaded_by = serializers.CharField()
    extra_fields = serializers.DictField(allow_null=True)


class PaginatedDataResponseSerializer(serializers.Serializer):
    """페이지네이션 응답 직렬화"""
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = UnifiedDataItemSerializer(many=True)
