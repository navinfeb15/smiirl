# Dockerfile
FROM python:3.9-slim

# install system deps for Playwright
RUN apt-get update && \
    apt-get install -y wget gnupg libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0 libx11-xcb1 libxss1 libxcursor1 libasound2 libpangocairo-1.0-0 libpango-1.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
