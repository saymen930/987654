FROM python:3.10-slim

# ffmpeg və digər tələbləri quraşdırırıq
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg gcc libffi-dev libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Bot fayllarını konteynerə kopyalayırıq
COPY . /app/
WORKDIR /app/

# Pip və requirements-ləri quraşdırırıq
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install --no-cache-dir --requirement requirements.txt

# Botu işə salırıq
CMD ["python3", "-m", "InflexMusic"]
