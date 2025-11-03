# -*- coding: utf-8 -*-
"""
Gunicorn 설정 파일

Railway 배포를 위한 Gunicorn 설정
모든 로그를 stdout으로 출력하여 Railway의 로그 레벨 오인식 방지
"""
import multiprocessing
import sys

# 서버 소켓
bind = "0.0.0.0:8080"

# 워커 설정
workers = 2
threads = 4
worker_class = "sync"
timeout = 120

# 로그 설정 - 모든 로그를 stdout으로
accesslog = "-"  # stdout
errorlog = "-"   # stdout
loglevel = "info"

# 로그 포맷
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Django WSGI 애플리케이션
wsgi_app = "config.wsgi:application"

# 프로세스 이름
proc_name = "django-app"

# 재시작 설정
max_requests = 1000
max_requests_jitter = 50

# Railway 환경에서 포트 동적 할당
import os
port = os.environ.get("PORT", "8080")
bind = f"0.0.0.0:{port}"
