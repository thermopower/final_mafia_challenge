# -*- coding: utf-8 -*-
"""
Student Repository

학생 데이터 접근 계층
"""
from typing import List, Dict, Optional
from django.db.models import Count, Q, Value
from django.db.models.functions import Coalesce
from django.db import transaction

from apps.dashboard.persistence.models import Student


class StudentRepository:
    """
    학생 데이터 Repository

    데이터베이스 CRUD 작업 및 통계 조회를 제공합니다.
    """

    @staticmethod
    def bulk_create(data_list: List[Dict]) -> int:
        """
        대량 데이터 삽입

        Args:
            data_list: 삽입할 데이터 리스트
                [
                    {
                        'student_id': '20201101',
                        'name': '김유진',
                        'college': '공과대학',
                        'department': '컴퓨터공학과',
                        'grade': 3,
                        'program_type': '학사',
                        'enrollment_status': '재학',
                        'gender': '남',
                        'admission_year': 2020,
                        'advisor': None,
                        'email': 'yjkim@university.ac.kr'
                    },
                    ...
                ]

        Returns:
            int: 삽입된 행 수
        """
        if not data_list:
            return 0

        with transaction.atomic():
            objects = [Student(**data) for data in data_list]
            created = Student.objects.bulk_create(
                objects,
                ignore_conflicts=False  # 중복 시 에러 발생
            )
            return len(created)

    @staticmethod
    def get_count_by_department(status: Optional[str] = None) -> List[Dict]:
        """
        학과별 학생 수 조회

        Args:
            status: 학적 상태 ('재학', '휴학', '졸업', None이면 전체)

        Returns:
            List[Dict]: 학과별 데이터
                [
                    {
                        'department': '컴퓨터공학과',
                        'count': 80
                    },
                    ...
                ]
        """
        queryset = Student.objects.all()

        if status:
            queryset = queryset.filter(enrollment_status=status)

        result = queryset.values('department').annotate(
            count=Count('id')
        ).order_by('-count')

        return list(result)

    @staticmethod
    def get_stats(status: str = '재학') -> Dict:
        """
        학생 통계 조회

        Args:
            status: 학적 상태 (기본값: '재학')

        Returns:
            Dict: 학생 통계
                {
                    'total_students': int,
                    'by_program': [
                        {'program_type': '학사', 'count': 280},
                        ...
                    ],
                    'by_status': [
                        {'enrollment_status': '재학', 'count': 290},
                        ...
                    ]
                }
        """
        # 재학생만 카운트
        total_students = Student.objects.filter(enrollment_status=status).count()

        by_program = list(
            Student.objects.filter(enrollment_status=status).values('program_type').annotate(
                count=Count('id')
            ).order_by('program_type')
        )

        by_status = list(
            Student.objects.values('enrollment_status').annotate(
                count=Count('id')
            ).order_by('enrollment_status')
        )

        return {
            'total_students': total_students,
            'by_program': by_program,
            'by_status': by_status
        }

    @staticmethod
    def get_by_program(status: str = '재학') -> List[Dict]:
        """
        과정별 학생 수 조회 (파이 차트용)

        Args:
            status: 학적 상태 (기본값: '재학')

        Returns:
            List[Dict]: 과정별 데이터
                [
                    {
                        'program_type': '학사',
                        'count': 280
                    },
                    ...
                ]
        """
        queryset = Student.objects.filter(enrollment_status=status)

        result = queryset.values('program_type').annotate(
            count=Count('id')
        ).order_by('program_type')

        return list(result)

    @staticmethod
    def delete_by_student_ids(student_ids: List[str]) -> int:
        """
        학번 목록으로 삭제

        Args:
            student_ids: 학번 리스트

        Returns:
            int: 삭제된 행 수
        """
        deleted_count, _ = Student.objects.filter(
            student_id__in=student_ids
        ).delete()

        return deleted_count
