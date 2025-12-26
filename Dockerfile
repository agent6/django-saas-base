FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

WORKDIR /app/backend

ENTRYPOINT ["/bin/sh", "-c", "python manage.py migrate && python manage.py ensure_initial_admin && exec \"$@\"", "--"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
