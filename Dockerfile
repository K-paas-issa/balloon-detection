# 베이스 이미지
FROM python:3.10.11

# 작업 디렉토리 설정
WORKDIR /app

# 빌드 도구 및 OpenCV 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libgl1-mesa-glx \
    && apt-get clean

# PyTorch와 torchvision 설치
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 요구 사항 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출 (다른 곳에서 접속 가능)
EXPOSE 8003

# 애플리케이션 실행
CMD ["uvicorn", "detection-server:app", "--host", "0.0.0.0", "--port", "8003"]