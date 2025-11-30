FROM python:3.9-slim

WORKDIR /app

# نصب dependencies سیستم
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# کپی و نصب requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کد برنامه
COPY . .

CMD ["python", "bot.py"]
