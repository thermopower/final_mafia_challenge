# -*- coding: utf-8 -*-
"""
Metric Calculator

지표 계산 로직
"""
from decimal import Decimal
from typing import Literal


class MetricCalculator:
    """
    지표 계산기

    순수 함수로 구성되어 있어 테스트가 용이합니다.
    """

    @staticmethod
    def calculate_change_rate(current_value: Decimal, previous_value: Decimal) -> Decimal:
        """
        전년 대비 증감률 계산

        Args:
            current_value: 현재 연도 값
            previous_value: 이전 연도 값

        Returns:
            Decimal: 증감률 (%) - 소수점 첫째 자리까지

        Raises:
            ValueError: previous_value가 0인 경우
        """
        if previous_value == Decimal('0.0'):
            raise ValueError('이전 값은 0이 될 수 없습니다')

        change_rate = ((current_value - previous_value) / previous_value) * Decimal('100.0')
        return round(change_rate, 1)

    @staticmethod
    def determine_trend(change_rate: Decimal) -> Literal['up', 'down', 'neutral']:
        """
        증감 추세 판단

        Args:
            change_rate: 증감률 (%)

        Returns:
            str: 'up' (증가), 'down' (감소), 'neutral' (동일)
        """
        if change_rate > Decimal('0.0'):
            return 'up'
        elif change_rate < Decimal('0.0'):
            return 'down'
        else:
            return 'neutral'
