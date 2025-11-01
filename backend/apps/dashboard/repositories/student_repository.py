# -*- coding: utf-8 -*-
"""
Student Repository

학생 데이터 접근 계층
"""
from typing import List
from django.db.models import Count

from apps.core.repositories.base_repository import BaseRepository
from apps.dashboard.persistence.models import Student as StudentORM
from apps.dashboard.domain.models import Student, StudentCount


class StudentRepository(BaseRepository):
    """
    학생 Repository

    ORM 쿼리를 도메인 모델로 변환합니다.
    """
    model = StudentORM

    def get_count_by_year(self, year: int, department: str = 'all') -> int:
        """
        연도별 학생 수 조회 (재학생만)

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            int: 재학생 수
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            status='active'
        )

        # 연도 필터 (student_id가 연도를 포함한다고 가정)
        # 예: student_id가 "2024001" 형식이라면
        queryset = queryset.filter(student_id__startswith=str(year))

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        return queryset.count()

    def get_count_by_department(self, year: int) -> List[StudentCount]:
        """
        학과별 학생 수 조회

        Args:
            year: 조회할 연도

        Returns:
            List[StudentCount]: 학과별 학생 수 리스트
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            status='active'
        )

        # 연도 필터
        queryset = queryset.filter(student_id__startswith=str(year))

        # 학과별 집계
        distribution = queryset.values('department').annotate(
            count=Count('id')
        ).order_by('-count')

        return [
            StudentCount(
                department=item['department'],
                count=item['count']
            )
            for item in distribution
        ]

    def get_all_by_year(self, year: int, department: str = 'all') -> List[Student]:
        """
        연도별 학생 전체 조회

        Args:
            year: 조회할 연도
            department: 부서명 (기본값: 'all')

        Returns:
            List[Student]: 학생 리스트
        """
        queryset = self.model.objects.filter(
            is_deleted=False,
            status='active',
            student_id__startswith=str(year)
        )

        # if department != 'all':
        #     queryset = queryset.filter(department=department)

        students = queryset.order_by('student_id')

        return [self._to_domain(student) for student in students]

    def _to_domain(self, orm_obj: StudentORM) -> Student:
        """ORM 모델 → 도메인 모델 변환"""
        return Student(
            id=orm_obj.id,
            department=orm_obj.department
        )

    def bulk_create(self, students: List[dict], user_id: str) -> int:
        """
        학생 데이터 배치 생성

        Args:
            students: 학생 데이터 리스트 (파싱된 딕셔너리)
            user_id: 업로드한 사용자 ID

        Returns:
            int: 생성된 행 수
        """
        from apps.accounts.persistence.models import UserProfile

        user = UserProfile.objects.get(id=user_id)

        student_objs = [
            StudentORM(
                student_id=student['student_id'],
                name=student['name'],
                department=student['department'],
                grade=student['grade'],
                status=student.get('status', 'active'),
                uploaded_by=user
            )
            for student in students
        ]

        StudentORM.objects.bulk_create(student_objs)
        return len(student_objs)

    def check_duplicates(self, students: List[dict]) -> List[dict]:
        """
        중복 데이터 확인

        Args:
            students: 학생 데이터 리스트

        Returns:
            List[dict]: 중복된 데이터 리스트
        """
        duplicates = []

        for student in students:
            exists = StudentORM.objects.filter(
                student_id=student['student_id'],
                is_deleted=False
            ).exists()

            if exists:
                duplicates.append(student)

        return duplicates

    def _to_orm(self, domain_obj: Student) -> StudentORM:
        """도메인 모델 → ORM 모델 변환"""
        # 이 메서드는 create/update 시 사용
        pass
