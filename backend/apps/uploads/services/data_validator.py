# -*- coding: utf-8 -*-
"""
데이터 검증기

CSV 파일에서 파싱된 데이터를 검증합니다.
"""
from typing import List, Dict, Tuple
from decimal import Decimal
import re


class DataValidator:
    """
    CSV 데이터 검증기

    데이터 타입별 비즈니스 규칙을 검증합니다.
    """

    @staticmethod
    def validate_department_kpi(data_list: List[Dict]) -> Tuple[bool, List[str]]:
        """
        학과 KPI 데이터 검증

        Args:
            data_list: 파싱된 데이터 리스트

        Returns:
            (검증 성공 여부, 오류 메시지 리스트)
        """
        errors = []

        # 파일 내 중복 검사 (평가년도 + 학과)
        seen_keys = set()

        for idx, data in enumerate(data_list, start=1):
            try:
                # 연도 범위 검증
                year = data['evaluation_year']
                if not (2020 <= year <= 2030):
                    errors.append(f"{idx}행: 평가년도는 2020~2030 범위여야 합니다: {year}")

                # 취업률 범위 검증
                rate = data['employment_rate']
                if not (Decimal('0') <= rate <= Decimal('100')):
                    errors.append(f"{idx}행: 취업률은 0~100 범위여야 합니다: {rate}")

                # 음수 검증
                if data['full_time_faculty'] < 0:
                    errors.append(f"{idx}행: 전임교원 수는 음수일 수 없습니다")
                if data['visiting_faculty'] < 0:
                    errors.append(f"{idx}행: 초빙교원 수는 음수일 수 없습니다")
                if data['tech_transfer_income'] < Decimal('0'):
                    errors.append(f"{idx}행: 기술이전 수입액은 음수일 수 없습니다")
                if data['intl_conferences'] < 0:
                    errors.append(f"{idx}행: 국제학술대회 개최 횟수는 음수일 수 없습니다")

                # 중복 검사
                key = (year, data['department'])
                if key in seen_keys:
                    errors.append(f"{idx}행: {year}년 {data['department']}는 이미 존재합니다")
                seen_keys.add(key)

            except (KeyError, TypeError) as e:
                errors.append(f"{idx}행 검증 오류: {str(e)}")

        return (len(errors) == 0, errors)

    @staticmethod
    def validate_publication(data_list: List[Dict]) -> Tuple[bool, List[str]]:
        """
        논문 데이터 검증

        Args:
            data_list: 파싱된 데이터 리스트

        Returns:
            (검증 성공 여부, 오류 메시지 리스트)
        """
        errors = []
        seen_paper_ids = set()

        for idx, data in enumerate(data_list, start=1):
            try:
                # 논문ID 형식 검증 (PUB-YY-NNN)
                paper_id = data['paper_id']
                if not re.match(r'^PUB-\d{2}-\d{3,}$', paper_id):
                    errors.append(f"{idx}행: 논문ID 형식이 올바르지 않습니다: {paper_id} (PUB-YY-NNN 필요)")

                # 논문ID 중복 검사
                if paper_id in seen_paper_ids:
                    errors.append(f"{idx}행: 논문ID가 이미 존재합니다: {paper_id}")
                seen_paper_ids.add(paper_id)

                # 저널 등급 검증
                grade = data['journal_grade']
                if grade not in ('SCIE', 'KCI'):
                    errors.append(f"{idx}행: 저널 등급은 SCIE 또는 KCI여야 합니다: {grade}")

                # Impact Factor 검증 (SCIE는 필수)
                if grade == 'SCIE' and data['impact_factor'] is None:
                    errors.append(f"{idx}행: SCIE 논문은 Impact Factor가 필수입니다")

                if data['impact_factor'] is not None and data['impact_factor'] < Decimal('0'):
                    errors.append(f"{idx}행: Impact Factor는 음수일 수 없습니다")

                # 과제연계여부 검증
                linked = data['project_linked']
                if linked not in ('Y', 'N'):
                    errors.append(f"{idx}행: 과제연계여부는 Y 또는 N이어야 합니다: {linked}")

                # 제목 길이 검증
                title = data['paper_title']
                if not (1 <= len(title) <= 500):
                    errors.append(f"{idx}행: 논문 제목은 1자 이상 500자 이하여야 합니다")

            except (KeyError, TypeError) as e:
                errors.append(f"{idx}행 검증 오류: {str(e)}")

        return (len(errors) == 0, errors)

    @staticmethod
    def validate_research_project(data_list: List[Dict]) -> Tuple[bool, List[str]]:
        """
        연구 과제 데이터 검증

        Args:
            data_list: 파싱된 데이터 리스트

        Returns:
            (검증 성공 여부, 오류 메시지 리스트)
        """
        errors = []
        seen_execution_ids = set()
        project_budgets = {}  # 과제번호별 총연구비 추적

        for idx, data in enumerate(data_list, start=1):
            try:
                # 집행ID 형식 검증 (T2324NNN)
                execution_id = data['execution_id']
                if not re.match(r'^T\d{4}\d{3,}$', execution_id):
                    errors.append(f"{idx}행: 집행ID 형식이 올바르지 않습니다: {execution_id} (T2324NNN 형식 필요)")

                # 집행ID 중복 검사
                if execution_id in seen_execution_ids:
                    errors.append(f"{idx}행: 집행ID가 이미 존재합니다: {execution_id}")
                seen_execution_ids.add(execution_id)

                # 예산 양수 검증
                if data['total_budget'] < 0:
                    errors.append(f"{idx}행: 총연구비는 음수일 수 없습니다")
                if data['execution_amount'] < 0:
                    errors.append(f"{idx}행: 집행금액은 음수일 수 없습니다")

                # 상태 검증
                status = data['status']
                if status not in ('집행완료', '처리중'):
                    errors.append(f"{idx}행: 상태는 '집행완료' 또는 '처리중'이어야 합니다: {status}")

                # 과제별 집행액 합계 추적
                project_number = data['project_number']
                if project_number not in project_budgets:
                    project_budgets[project_number] = {
                        'total_budget': data['total_budget'],
                        'execution_sum': 0
                    }
                project_budgets[project_number]['execution_sum'] += data['execution_amount']

            except (KeyError, TypeError) as e:
                errors.append(f"{idx}행 검증 오류: {str(e)}")

        # 과제별 집행액 합계 vs 총연구비 검증
        for project_number, budget_info in project_budgets.items():
            if budget_info['execution_sum'] > budget_info['total_budget']:
                errors.append(
                    f"과제 {project_number}의 집행액 합계({budget_info['execution_sum']})가 "
                    f"총연구비({budget_info['total_budget']})를 초과합니다"
                )

        return (len(errors) == 0, errors)

    @staticmethod
    def validate_student_roster(data_list: List[Dict]) -> Tuple[bool, List[str]]:
        """
        학생 명단 데이터 검증

        Args:
            data_list: 파싱된 데이터 리스트

        Returns:
            (검증 성공 여부, 오류 메시지 리스트)
        """
        errors = []
        seen_student_ids = set()

        for idx, data in enumerate(data_list, start=1):
            try:
                # 학번 형식 검증 (YYYYMMNNN)
                student_id = data['student_id']
                if not re.match(r'^\d{8,9}$', student_id):
                    errors.append(f"{idx}행: 학번 형식이 올바르지 않습니다: {student_id} (YYYYMMNNN 필요)")

                # 학번 중복 검사
                if student_id in seen_student_ids:
                    errors.append(f"{idx}행: 학번이 이미 존재합니다: {student_id}")
                seen_student_ids.add(student_id)

                # 이름 길이 검증
                name = data['name']
                if not (2 <= len(name) <= 50):
                    errors.append(f"{idx}행: 이름은 2자 이상 50자 이하여야 합니다: {name}")

                # 학년 범위 검증
                grade = data['grade']
                if not (0 <= grade <= 4):
                    errors.append(f"{idx}행: 학년은 0~4 범위여야 합니다: {grade}")

                # 과정구분 검증
                program_type = data['program_type']
                if program_type not in ('학사', '석사', '박사'):
                    errors.append(f"{idx}행: 과정구분은 학사, 석사, 박사 중 하나여야 합니다: {program_type}")

                # 학년-과정 일치성 검증
                if program_type in ('석사', '박사') and grade != 0:
                    errors.append(f"{idx}행: 석사/박사는 학년이 0이어야 합니다: {program_type}, {grade}")

                # 학적상태 검증
                status = data['enrollment_status']
                if status not in ('재학', '휴학', '졸업'):
                    errors.append(f"{idx}행: 학적상태는 재학, 휴학, 졸업 중 하나여야 합니다: {status}")

                # 성별 검증
                gender = data['gender']
                if gender not in ('남', '여'):
                    errors.append(f"{idx}행: 성별은 남 또는 여여야 합니다: {gender}")

                # 입학년도 범위 검증
                admission_year = data['admission_year']
                if not (2015 <= admission_year <= 2025):
                    errors.append(f"{idx}행: 입학년도는 2015~2025 범위여야 합니다: {admission_year}")

                # 이메일 형식 검증
                email = data['email']
                if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                    errors.append(f"{idx}행: 이메일 형식이 올바르지 않습니다: {email}")

            except (KeyError, TypeError) as e:
                errors.append(f"{idx}행 검증 오류: {str(e)}")

        return (len(errors) == 0, errors)
