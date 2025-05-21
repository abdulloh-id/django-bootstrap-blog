FROM python:3.11-alpine

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache mariadb-dev gcc musl-dev

# Install pip dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir mysqlclient==2.2.7 && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Make port 8000 available
EXPOSE 8000

# Define environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]