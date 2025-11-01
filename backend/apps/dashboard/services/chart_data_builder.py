# -*- coding: utf-8 -*-
"""
Chart Data Builder

차트 데이터 생성 로직
"""
from typing import List, Dict, Any
from decimal import Decimal

from apps.dashboard.domain.models import (
    Performance,
    PaperCount,
    StudentCount,
    BudgetRatio
)


class ChartDataBuilder:
    """
    차트 데이터 빌더

    Backend 데이터를 Frontend 차트 형식으로 변환합니다.
    """

    @staticmethod
    def build_performance_trend(performances: List[Performance]) -> List[Dict[str, Any]]:
        """
        실적 추세 라인 차트 데이터 생성

        Args:
            performances: 실적 리스트

        Returns:
            List[Dict]: [{"month": "1월", "value": 12.5}, ...]
        """
        result = []
        for perf in performances:
            result.append({
                'month': f'{perf.month}월',
                'value': perf.amount
            })
        return result

    @staticmethod
    def build_paper_distribution(paper_counts: List[PaperCount]) -> List[Dict[str, Any]]:
        """
        논문 분포 막대 차트 데이터 생성

        Args:
            paper_counts: 카테고리별 논문 수 리스트

        Returns:
            List[Dict]: [{"category": "SCI", "count": 120}, ...]
        """
        result = []
        for pc in paper_counts:
            result.append({
                'category': pc.category,
                'count': pc.count
            })
        return result

    @staticmethod
    def build_budget_ratio(budget_ratios: List[BudgetRatio]) -> List[Dict[str, Any]]:
        """
        예산 비율 파이 차트 데이터 생성

        Args:
            budget_ratios: 카테고리별 예산 비율 리스트

        Returns:
            List[Dict]: [{"category": "인건비", "value": 45.2, "percentage": 51.7}, ...]
        """
        result = []
        for br in budget_ratios:
            result.append({
                'category': br.category,
                'value': br.amount,
                'percentage': br.percentage
            })
        return result

    @staticmethod
    def build_student_count(student_counts: List[StudentCount]) -> List[Dict[str, Any]]:
        """
        학생 수 막대 차트 데이터 생성

        Args:
            student_counts: 학과별 학생 수 리스트

        Returns:
            List[Dict]: [{"department": "컴퓨터공학과", "count": 450}, ...]
        """
        result = []
        for sc in student_counts:
            result.append({
                'department': sc.department,
                'count': sc.count
            })
        return result
