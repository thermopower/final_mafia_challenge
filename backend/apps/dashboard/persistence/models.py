# -*- coding: utf-8 -*-
"""
Dashboard Persistence 모델

Django ORM 모델 정의 (데이터베이스 스키마와 직접 매핑)
실제 CSV 파일 구조와 database.md 스키마에 정확히 일치하도록 작성
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel


class Performance(TimeStampedModel):
    """
    실적 데이터 ORM 모델 (레거시)

    임시 모델 - 향후 DepartmentKPI로 통합 예정

    Attributes:
        date: 실적 날짜
        amount: 실적 금액
        category: 실적 분류
        department: 부서명
    """
    date = models.DateField(
        verbose_name="실적 날짜"
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="실적 금액"
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="실적 분류"
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="부서명"
    )

    class Meta:
        db_table = 'performance'
        verbose_name = '실적'
        verbose_name_plural = '실적 목록'
        indexes = [
            models.Index(fields=['date'], name='idx_perf_date'),
            models.Index(fields=['department'], name='idx_perf_dept'),
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.amount}"


class DepartmentKPI(TimeStampedModel):
    """
    학과 KPI 데이터 ORM 모델

    CSV: department_kpi.csv

    평가년도별 학과 성과 지표 저장
    취업률, 교원 수, 기술이전 수입, 학술대회 개최 횟수 등

    Attributes:
        evaluation_year: 평가년도 (2020~2030)
        college: 단과대학명
        department: 학과명
        employment_rate: 졸업생 취업률 (%, 0~100)
        full_time_faculty: 전임교원 수 (명)
        visiting_faculty: 초빙교원 수 (명)
        tech_transfer_income: 기술이전 수입액 (억원)
        intl_conferences: 국제학술대회 개최 횟수
    """
    evaluation_year = models.IntegerField(
        verbose_name="평가년도",
        help_text="2020~2030 범위"
    )
    college = models.CharField(
        max_length=100,
        verbose_name="단과대학"
    )
    department = models.CharField(
        max_length=100,
        verbose_name="학과"
    )
    employment_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="졸업생 취업률",
        help_text="%, 소수점 2자리"
    )
    full_time_faculty = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="전임교원 수",
        help_text="명"
    )
    visiting_faculty = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="초빙교원 수",
        help_text="명"
    )
    tech_transfer_income = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        validators=[MinValueValidator(0)],
        verbose_name="기술이전 수입액",
        help_text="억원 단위"
    )
    intl_conferences = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="국제학술대회 개최 횟수"
    )

    class Meta:
        db_table = 'department_kpi'
        verbose_name = '학과 KPI 데이터'
        verbose_name_plural = '학과 KPI 데이터 목록'
        constraints = [
            models.UniqueConstraint(
                fields=['evaluation_year', 'department'],
                name='uk_department_kpi_year_dept'
            )
        ]
        indexes = [
            models.Index(fields=['evaluation_year'], name='idx_dept_kpi_year'),
            models.Index(fields=['department'], name='idx_dept_kpi_dept'),
            models.Index(fields=['college'], name='idx_dept_kpi_college'),
            models.Index(fields=['evaluation_year', 'college'], name='idx_dept_kpi_year_college'),
            models.Index(fields=['created_at'], name='idx_dept_kpi_created'),
        ]
        ordering = ['-evaluation_year', 'college', 'department']

    def __str__(self):
        return f"{self.evaluation_year}년 {self.department}"


class Publication(TimeStampedModel):
    """
    논문 목록 ORM 모델

    CSV: publication_list.csv

    학술지 게재 논문 정보 저장

    Attributes:
        paper_id: 논문 고유 ID (PUB-YY-NNN 형식)
        publication_date: 게재일
        college: 단과대학
        department: 학과
        paper_title: 논문 제목 (1~500자)
        lead_author: 주저자
        co_authors: 참여저자 (세미콜론으로 구분)
        journal_name: 학술지명
        journal_grade: 저널 등급 (SCIE/KCI)
        impact_factor: Impact Factor (SCIE만 필수, KCI는 NULL)
        project_linked: 과제연계여부 (Y/N)
    """
    paper_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="논문ID",
        help_text="PUB-YY-NNN 형식"
    )
    publication_date = models.DateField(
        verbose_name="게재일"
    )
    college = models.CharField(
        max_length=100,
        verbose_name="단과대학"
    )
    department = models.CharField(
        max_length=100,
        verbose_name="학과"
    )
    paper_title = models.TextField(
        verbose_name="논문 제목",
        help_text="1~500자"
    )
    lead_author = models.CharField(
        max_length=100,
        verbose_name="주저자"
    )
    co_authors = models.TextField(
        blank=True,
        null=True,
        verbose_name="참여저자",
        help_text="세미콜론으로 구분"
    )
    journal_name = models.CharField(
        max_length=200,
        verbose_name="학술지명"
    )
    journal_grade = models.CharField(
        max_length=10,
        choices=[
            ('SCIE', 'SCIE'),
            ('KCI', 'KCI'),
        ],
        verbose_name="저널 등급"
    )
    impact_factor = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Impact Factor",
        help_text="SCIE만 필수, KCI는 NULL"
    )
    project_linked = models.CharField(
        max_length=1,
        choices=[
            ('Y', '연계'),
            ('N', '비연계'),
        ],
        verbose_name="과제연계여부"
    )

    class Meta:
        db_table = 'publication'
        verbose_name = '논문'
        verbose_name_plural = '논문 목록'
        indexes = [
            models.Index(fields=['publication_date'], name='idx_pub_date'),
            models.Index(fields=['department'], name='idx_pub_dept'),
            models.Index(fields=['college'], name='idx_pub_college'),
            models.Index(fields=['journal_grade'], name='idx_pub_grade'),
            models.Index(fields=['project_linked'], name='idx_pub_linked'),
            models.Index(fields=['created_at'], name='idx_pub_created'),
        ]
        ordering = ['-publication_date']

    def __str__(self):
        return f"{self.paper_id} - {self.paper_title[:50]}"


# 하위 호환성을 위한 별칭
Paper = Publication


class ResearchProject(TimeStampedModel):
    """
    연구 과제 데이터 ORM 모델

    CSV: research_project_data.csv

    연구 과제별 예산 집행 현황 저장

    Attributes:
        execution_id: 집행 고유 ID (T2324NNN 형식)
        project_number: 과제번호 (예: NRF-2023-015)
        project_name: 과제명
        principal_investigator: 연구책임자
        department: 소속학과
        funding_agency: 지원기관
        total_budget: 총 연구비 (원 단위)
        execution_date: 집행일자
        execution_item: 집행 항목
        execution_amount: 집행 금액 (원 단위)
        status: 집행 상태 (집행완료/처리중)
        remarks: 비고 (nullable)
    """
    execution_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="집행ID",
        help_text="T2324NNN 형식"
    )
    project_number = models.CharField(
        max_length=100,
        verbose_name="과제번호",
        help_text="예: NRF-2023-015"
    )
    project_name = models.CharField(
        max_length=200,
        verbose_name="과제명"
    )
    principal_investigator = models.CharField(
        max_length=100,
        verbose_name="연구책임자"
    )
    department = models.CharField(
        max_length=100,
        verbose_name="소속학과"
    )
    funding_agency = models.CharField(
        max_length=100,
        verbose_name="지원기관"
    )
    total_budget = models.BigIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="총 연구비",
        help_text="원 단위"
    )
    execution_date = models.DateField(
        verbose_name="집행일자"
    )
    execution_item = models.CharField(
        max_length=200,
        verbose_name="집행 항목"
    )
    execution_amount = models.BigIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="집행 금액",
        help_text="원 단위"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('집행완료', '집행완료'),
            ('처리중', '처리중'),
        ],
        verbose_name="상태"
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name="비고"
    )

    class Meta:
        db_table = 'research_project'
        verbose_name = '연구 과제'
        verbose_name_plural = '연구 과제 목록'
        indexes = [
            models.Index(fields=['project_number'], name='idx_rp_project_number'),
            models.Index(fields=['principal_investigator'], name='idx_rp_pi'),
            models.Index(fields=['department'], name='idx_rp_dept'),
            models.Index(fields=['funding_agency'], name='idx_rp_agency'),
            models.Index(fields=['execution_date'], name='idx_rp_date'),
            models.Index(fields=['status'], name='idx_rp_status'),
            models.Index(fields=['project_number', 'execution_date'], name='idx_rp_project_date'),
            models.Index(fields=['execution_item'], name='idx_rp_item'),
        ]
        ordering = ['-execution_date']

    def __str__(self):
        return f"{self.execution_id} - {self.project_name}"


class Student(TimeStampedModel):
    """
    학생 명단 ORM 모델

    CSV: student_roster.csv

    학생 기본 정보 및 학적 상태 저장

    Attributes:
        student_id: 학번 (YYYYMMNNN 형식)
        name: 이름 (2~50자)
        college: 단과대학
        department: 학과
        grade: 학년 (학사: 1~4, 석사/박사: 0)
        program_type: 과정 구분 (학사/석사/박사)
        enrollment_status: 학적 상태 (재학/휴학/졸업)
        gender: 성별 (남/여)
        admission_year: 입학년도 (2015~2025)
        advisor: 지도교수 (학부생은 NULL 가능)
        email: 이메일
    """
    student_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="학번",
        help_text="YYYYMMNNN 형식"
    )
    name = models.CharField(
        max_length=50,
        verbose_name="이름"
    )
    college = models.CharField(
        max_length=100,
        verbose_name="단과대학"
    )
    department = models.CharField(
        max_length=100,
        verbose_name="학과"
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        verbose_name="학년",
        help_text="학사: 1~4, 석사/박사: 0"
    )
    program_type = models.CharField(
        max_length=10,
        choices=[
            ('학사', '학사'),
            ('석사', '석사'),
            ('박사', '박사'),
        ],
        verbose_name="과정 구분"
    )
    enrollment_status = models.CharField(
        max_length=10,
        choices=[
            ('재학', '재학'),
            ('휴학', '휴학'),
            ('졸업', '졸업'),
        ],
        verbose_name="학적 상태"
    )
    gender = models.CharField(
        max_length=1,
        choices=[
            ('남', '남'),
            ('여', '여'),
        ],
        verbose_name="성별"
    )
    admission_year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2025)],
        verbose_name="입학년도",
        help_text="2015~2025"
    )
    advisor = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="지도교수",
        help_text="학부생은 NULL 가능"
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="이메일"
    )

    class Meta:
        db_table = 'student'
        verbose_name = '학생'
        verbose_name_plural = '학생 목록'
        indexes = [
            models.Index(fields=['department'], name='idx_student_dept'),
            models.Index(fields=['college'], name='idx_student_college'),
            models.Index(fields=['program_type'], name='idx_student_program'),
            models.Index(fields=['enrollment_status'], name='idx_student_status'),
            models.Index(fields=['grade'], name='idx_student_grade'),
            models.Index(fields=['admission_year'], name='idx_student_admission'),
            models.Index(fields=['department', 'enrollment_status'], name='idx_student_dept_status'),
            models.Index(fields=['gender'], name='idx_student_gender'),
        ]
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.name}"
