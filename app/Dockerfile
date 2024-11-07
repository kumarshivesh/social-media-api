# app/Dockerfile
# FastAPI Dockerfile

# Pull python base image
FROM python:3.11.4-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV HOME=/home/app
ENV APP_HOME=${HOME}/web

# Create app user and necessary directories
RUN mkdir -p $HOME && \
    addgroup --system app && \
    adduser --system --group app && \
    mkdir $APP_HOME

# Set work directory
WORKDIR $APP_HOME

# Copy requirements.txt
COPY ./requirements.txt $APP_HOME

# Install python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install other dependencies (Debian)
RUN apt-get update && apt-get install -y --no-install-recommends netcat curl && rm -rf /var/lib/apt/lists/*

# Copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# Ensure entrypoint.sh has correct permissions
RUN chmod +x ${APP_HOME}/entrypoint.sh \
    && sed -i 's/\r$//' ${APP_HOME}/entrypoint.sh \
    && ls -l ${APP_HOME}/entrypoint.sh  # Debug: verify permissions

# Copy project files
COPY . $APP_HOME

# Switch to app user
USER app

# Expose port 8000
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=5s \
            --timeout=3s \
            CMD curl --fail http://localhost:8000/ || exit 1

# Run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

# Run application with Gunicorn
CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "app.main:app"]
