# -*- coding: utf-8 -*-
"""
Dashboard Serializers

API 응답 직렬화
"""

from rest_framework import serializers
from datetime import datetime


class KPIMetricSerializer(serializers.Serializer):
    """
    단일 KPI 메트릭 직렬화

    {
        "value": 150,
        "change_rate": 5.2
    }
    """
    value = serializers.FloatField()
    change_rate = serializers.FloatField()


class ChartDataItemSerializer(serializers.Serializer):
    """
    차트 데이터 항목 직렬화 (범용)

    동적 필드를 허용하기 위해 pass
    """
    pass


class DashboardResponseSerializer(serializers.Serializer):
    """
    대시보드 전체 응답 직렬화

    GET /api/dashboard/ 응답 형식

    {
        "kpi_metrics": {
            "full_time_faculty": {"value": 150, "change_rate": 5.2},
            "visiting_faculty": {"value": 30, "change_rate": -2.1},
            "employment_rate": {"value": 85.3, "change_rate": 1.5},
            "tech_transfer_income": {"value": 120.0, "change_rate": 10.3},
            "total_papers": {"value": 250, "change_rate": 8.7},
            "avg_impact_factor": {"value": 3.45, "change_rate": 0.2},
            "total_students": {"value": 1200, "change_rate": 3.1},
            "budget_execution_rate": {"value": 92.5, "change_rate": -1.2}
        },
        "charts": {
            "department_employment_rate": [
                {"department": "컴퓨터공학과", "rate": 90.5},
                ...
            ],
            "faculty_trend": [
                {"year": 2024, "full_time": 150, "visiting": 30},
                ...
            ],
            "tech_transfer_trend": [
                {"year": 2024, "income": 120.0},
                ...
            ],
            "paper_distribution": [
                {"grade": "SCIE", "count": 30},
                ...
            ],
            "papers_by_department": [
                {"department": "컴퓨터공학과", "count": 10},
                ...
            ],
            "students_by_program": [
                {"program": "학사", "count": 280},
                ...
            ],
            "students_by_department": [
                {"department": "컴퓨터공학과", "count": 80},
                ...
            ],
            "budget_by_item": [
                {"item": "연구장비 도입", "amount": 150000000},
                ...
            ],
            "budget_by_funder": [
                {"funder": "한국연구재단", "amount": 500000000},
                ...
            ]
        }
    }
    """
    kpi_metrics = serializers.DictField(
        child=KPIMetricSerializer()
    )
    charts = serializers.DictField(
        child=serializers.ListField(
            child=serializers.DictField()
        )
    )


class DashboardFilterSerializer(serializers.Serializer):
    """
    대시보드 필터 파라미터 검증

    Query Parameters:
        year: 연도 (기본값: 현재 연도)
        college: 단과대학 (기본값: 'all')
    """
    year = serializers.IntegerField(
        required=False,
        min_value=2020,
        max_value=datetime.now().year + 1,
        default=datetime.now().year
    )
    college = serializers.CharField(
        required=False,
        max_length=100,
        default='all'
    )

    def validate_college(self, value):
        """
        단과대학 값 검증

        Args:
            value: 단과대학 값

        Returns:
            str: 검증된 값
        """
        # 'all'은 항상 허용
        if value == 'all':
            return value

        # TODO: 실제 단과대학 목록으로 검증 (필요 시)
        # valid_colleges = ['공과대학', '경영대학', '인문대학', ...]
        # if value not in valid_colleges:
        #     raise serializers.ValidationError(f"유효하지 않은 단과대학입니다: {value}")

        return value
