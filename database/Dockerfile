FROM python:3.12-slim

WORKDIR /app

# Install PostgreSQL client so we can run psql scripts
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install backend Python dependencies (needed by app.models / app.db)
COPY backend/requirements.txt ./backend-requirements.txt
RUN pip install --no-cache-dir -r backend-requirements.txt

# Copy backend app package and database scripts (including JSON data)
COPY backend/app ./app
COPY database ./database

ENV PYTHONPATH=/app
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_USER=ksi_opinion_base
ENV DB_PASSWORD=ksi_opinion_base
ENV DB_NAME=ksi_opinion_base

WORKDIR /app/database

# Strip any Windows CRLF line endings so the shebang works on every host
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

ENTRYPOINT ["/app/database/entrypoint.sh"]
