#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
테스트 데이터 Import 스크립트

docs/inputdata/ 폴더의 CSV 파일들을 데이터베이스에 import합니다.
"""
import os
import sys
import django
import csv
from decimal import Decimal
from datetime import datetime

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.dashboard.persistence.models import DepartmentKPI, Publication, Student, ResearchProject


def import_department_kpi():
    """학과 KPI 데이터 import"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'inputdata', 'department_kpi.csv')

    print(f"[DepartmentKPI] CSV 파일 읽기: {csv_path}")

    # 기존 데이터 삭제
    existing_count = DepartmentKPI.objects.count()
    if existing_count > 0:
        print(f"[DepartmentKPI] 기존 {existing_count}개 레코드 삭제")
        DepartmentKPI.objects.all().delete()

    if not os.path.exists(csv_path):
        print(f"파일이 존재하지 않습니다: {csv_path}")
        return

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0

        for row in reader:
            DepartmentKPI.objects.create(
                evaluation_year=int(row['평가년도']),
                college=row['단과대학'],
                department=row['학과'],
                employment_rate=Decimal(row['졸업생 취업률 (%)']),
                full_time_faculty=int(row['전임교원 수 (명)']),
                visiting_faculty=int(row['초빙교원 수 (명)']),
                tech_transfer_income=Decimal(row['연간 기술이전 수입액 (억원)']),
                intl_conferences=int(row['국제학술대회 개최 횟수'])
            )
            count += 1

    print(f"[DepartmentKPI] {count}개 레코드 import 완료")


def import_publications():
    """논문 데이터 import"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'inputdata', 'publication_list.csv')

    print(f"[Publication] CSV 파일 읽기: {csv_path}")

    # 기존 데이터 삭제
    existing_count = Publication.objects.count()
    if existing_count > 0:
        print(f"[Publication] 기존 {existing_count}개 레코드 삭제")
        Publication.objects.all().delete()

    if not os.path.exists(csv_path):
        print(f"파일이 존재하지 않습니다: {csv_path}")
        return

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0

        for row in reader:
            # Impact Factor: 빈 문자열이면 None
            impact_factor = None
            if row['Impact Factor'].strip():
                try:
                    impact_factor = Decimal(row['Impact Factor'])
                except:
                    impact_factor = None

            Publication.objects.create(
                paper_id=row['논문ID'],
                publication_date=datetime.strptime(row['게재일'], '%Y-%m-%d').date(),
                college=row['단과대학'],
                department=row['학과'],
                paper_title=row['논문제목'],
                lead_author=row['주저자'],
                co_authors=row['참여저자'] if row['참여저자'] else None,
                journal_name=row['학술지명'],
                journal_grade=row['저널등급'],
                impact_factor=impact_factor,
                project_linked=row['과제연계여부']
            )
            count += 1

    print(f"[Publication] {count}개 레코드 import 완료")


def import_research_projects():
    """연구 과제 데이터 import"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'inputdata', 'research_project_data.csv')

    print(f"[ResearchProject] CSV 파일 읽기: {csv_path}")

    # 기존 데이터 삭제
    existing_count = ResearchProject.objects.count()
    if existing_count > 0:
        print(f"[ResearchProject] 기존 {existing_count}개 레코드 삭제")
        ResearchProject.objects.all().delete()

    if not os.path.exists(csv_path):
        print(f"파일이 존재하지 않습니다: {csv_path}")
        return

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0

        for row in reader:
            ResearchProject.objects.create(
                execution_id=row['집행ID'],
                project_number=row['과제번호'],
                project_name=row['과제명'],
                principal_investigator=row['연구책임자'],
                department=row['소속학과'],
                funding_agency=row['지원기관'],
                total_budget=int(row['총연구비']),
                execution_date=datetime.strptime(row['집행일자'], '%Y-%m-%d').date(),
                execution_item=row['집행항목'],
                execution_amount=int(row['집행금액']),
                status=row['상태'],
                remarks=row['비고'] if row['비고'] else None
            )
            count += 1

    print(f"[ResearchProject] {count}개 레코드 import 완료")


def import_students():
    """학생 데이터 import (이미 있으면 스킵)"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'inputdata', 'student_roster.csv')

    print(f"[Student] CSV 파일 읽기: {csv_path}")

    if Student.objects.count() > 0:
        print(f"[Student] 이미 {Student.objects.count()}개 레코드가 존재합니다. 스킵합니다.")
        return

    if not os.path.exists(csv_path):
        print(f"파일이 존재하지 않습니다: {csv_path}")
        return

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0

        for row in reader:
            Student.objects.create(
                student_id=row['학번'],
                name=row['이름'],
                college=row['단과대학'],
                department=row['학과'],
                grade=int(row['학년']),
                program_type=row['과정구분'],
                enrollment_status=row['학적 상태'],
                gender=row['성별'],
                admission_year=int(row['입학년도']),
                advisor=row['지도교수'] if row['지도교수'] else None,
                email=row['이메일']
            )
            count += 1

    print(f"[Student] {count}개 레코드 import 완료")


if __name__ == '__main__':
    print("=" * 60)
    print("테스트 데이터 Import 시작")
    print("=" * 60)

    try:
        import_department_kpi()
        import_publications()
        import_research_projects()
        import_students()

        print("=" * 60)
        print("Import 완료!")
        print("=" * 60)

        # 최종 카운트 확인
        print(f"\n최종 데이터 개수:")
        print(f"  - DepartmentKPI: {DepartmentKPI.objects.count()}개")
        print(f"  - Publication: {Publication.objects.count()}개")
        print(f"  - ResearchProject: {ResearchProject.objects.count()}개")
        print(f"  - Student: {Student.objects.count()}개")

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
