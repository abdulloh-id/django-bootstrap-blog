FROM python:3.11-alpine
WORKDIR /app

# Install build dependencies (add postgresql-dev for psycopg2)
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Install pip dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Make port 8000 available
EXPOSE 8000

# Define environment variables for runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run migrations at startup, then start gunicorn
CMD python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000