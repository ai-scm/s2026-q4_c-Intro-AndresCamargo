FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir mlflow==2.16.2 sqlalchemy==2.0.36 scikit-learn==1.5.2 pandas==2.2.3 numpy==1.26.4
COPY train.py .
