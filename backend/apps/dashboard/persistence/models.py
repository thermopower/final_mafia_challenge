# -*- coding: utf-8 -*-
"""
Dashboard Persistence 모델

Django ORM 모델 정의 (데이터베이스 스키마와 직접 매핑)
"""
from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel


class Performance(TimeStampedModel):
    """
    실적 데이터 ORM 모델

    Attributes:
        date: 실적 발생 날짜
        title: 실적 항목명
        amount: 금액 (원)
        category: 카테고리
        description: 상세 설명
        uploaded_by: 업로드한 사용자 (외래키)
        is_deleted: 소프트 삭제 플래그
    """
    date = models.DateField(verbose_name="실적 발생 날짜")
    title = models.CharField(max_length=255, verbose_name="실적 항목명")
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="금액"
    )
    category = models.CharField(max_length=100, verbose_name="카테고리")
    description = models.TextField(blank=True, null=True, verbose_name="상세 설명")
    uploaded_by = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.RESTRICT,
        related_name='performances',
        verbose_name="업로드한 사용자"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="삭제 여부")

    class Meta:
        db_table = 'performances'
        verbose_name = '실적'
        verbose_name_plural = '실적 목록'
        indexes = [
            models.Index(fields=['date', 'category']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_deleted']),
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.amount}원)"


class Paper(TimeStampedModel):
    """
    논문 데이터 ORM 모델

    Attributes:
        title: 논문 제목
        authors: 저자 목록
        publication_date: 게재일
        field: 분야
        journal_name: 학술지명
        doi: DOI
        uploaded_by: 업로드한 사용자
        is_deleted: 소프트 삭제 플래그
    """
    title = models.CharField(max_length=500, verbose_name="논문 제목")
    authors = models.TextField(verbose_name="저자 목록")
    publication_date = models.DateField(verbose_name="게재일")
    field = models.CharField(max_length=100, verbose_name="분야")
    journal_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="학술지명")
    doi = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="DOI")
    uploaded_by = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.RESTRICT,
        related_name='papers',
        verbose_name="업로드한 사용자"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="삭제 여부")

    class Meta:
        db_table = 'papers'
        verbose_name = '논문'
        verbose_name_plural = '논문 목록'
        indexes = [
            models.Index(fields=['publication_date', 'field']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_deleted']),
        ]
        ordering = ['-publication_date']

    def __str__(self):
        return self.title


class Student(TimeStampedModel):
    """
    학생 데이터 ORM 모델

    Attributes:
        student_id: 학번
        name: 학생 이름
        department: 학과
        grade: 학년
        status: 상태
        uploaded_by: 업로드한 사용자
        is_deleted: 소프트 삭제 플래그
    """
    student_id = models.CharField(max_length=20, unique=True, verbose_name="학번")
    name = models.CharField(max_length=100, verbose_name="학생 이름")
    department = models.CharField(max_length=100, verbose_name="학과")
    grade = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="학년")
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', '재학'),
            ('graduated', '졸업'),
            ('withdrawn', '자퇴')
        ],
        default='active',
        verbose_name="상태"
    )
    uploaded_by = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.RESTRICT,
        related_name='students',
        verbose_name="업로드한 사용자"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="삭제 여부")

    class Meta:
        db_table = 'students'
        verbose_name = '학생'
        verbose_name_plural = '학생 목록'
        indexes = [
            models.Index(fields=['department', 'grade']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_deleted']),
        ]
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class Budget(TimeStampedModel):
    """
    예산 데이터 ORM 모델

    Attributes:
        item: 예산 항목명
        amount: 금액
        category: 카테고리
        fiscal_year: 회계연도
        quarter: 분기
        description: 상세 설명
        uploaded_by: 업로드한 사용자
        is_deleted: 소프트 삭제 플래그
    """
    item = models.CharField(max_length=255, verbose_name="예산 항목명")
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="금액"
    )
    category = models.CharField(max_length=100, verbose_name="카테고리")
    fiscal_year = models.IntegerField(verbose_name="회계연도")
    quarter = models.IntegerField(blank=True, null=True, verbose_name="분기")
    description = models.TextField(blank=True, null=True, verbose_name="상세 설명")
    uploaded_by = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.RESTRICT,
        related_name='budgets',
        verbose_name="업로드한 사용자"
    )
    is_deleted = models.BooleanField(default=False, verbose_name="삭제 여부")

    class Meta:
        db_table = 'budgets'
        verbose_name = '예산'
        verbose_name_plural = '예산 목록'
        indexes = [
            models.Index(fields=['fiscal_year', 'category']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_deleted']),
        ]
        ordering = ['-fiscal_year', '-quarter']

    def __str__(self):
        return f"{self.item} ({self.fiscal_year}년)"
