# -*- coding: utf-8 -*-
"""
Dashboard Serializers
"""

from rest_framework import serializers
from datetime import datetime


class DashboardMetricSerializer(serializers.Serializer):
    """대시보드 메트릭 직렬화"""
    label = serializers.CharField()
    value = serializers.DecimalField(max_digits=15, decimal_places=2)
    change = serializers.FloatField(required=False)


class ChartDataSerializer(serializers.Serializer):
    """차트 데이터 직렬화"""
    labels = serializers.ListField(child=serializers.CharField())
    datasets = serializers.ListField(child=serializers.DictField())


class DashboardSerializer(serializers.Serializer):
    """대시보드 전체 응답 직렬화"""
    metrics = serializers.ListField(child=DashboardMetricSerializer())
    charts = serializers.DictField(child=ChartDataSerializer())


class FilterParamsSerializer(serializers.Serializer):
    """대시보드 필터 파라미터 검증"""
    year = serializers.IntegerField(required=False, min_value=2000, max_value=datetime.now().year + 1)
    department = serializers.CharField(required=False, max_length=100)


class DashboardResponseSerializer(serializers.Serializer):
    """대시보드 응답 직렬화 (DashboardSerializer와 동일)"""
    metrics = serializers.ListField(child=DashboardMetricSerializer())
    charts = serializers.DictField(child=ChartDataSerializer())
