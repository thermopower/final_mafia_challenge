# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일시')),
                ('filename', models.CharField(max_length=255, verbose_name='파일명')),
                ('data_type', models.CharField(choices=[('performance', '실적'), ('paper', '논문'), ('student', '학생'), ('budget', '예산')], max_length=50, verbose_name='데이터 유형')),
                ('rows_processed', models.IntegerField(default=0, verbose_name='처리된 행 수')),
                ('uploaded_by', models.CharField(max_length=255, verbose_name='업로드 사용자 이메일')),
                ('status', models.CharField(choices=[('success', '성공'), ('failed', '실패'), ('partial', '부분 성공')], max_length=20, verbose_name='상태')),
            ],
            options={
                'verbose_name': '업로드된 파일',
                'verbose_name_plural': '업로드된 파일 목록',
                'db_table': 'uploaded_files',
                'ordering': ['-created_at'],
            },
        ),
    ]
