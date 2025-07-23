FROM python:3.10-slim

# Node.js üçün lazım olan dependensiyalar və Node.js 18 quraşdırılır
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ffmpeg bash git gnupg ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN pip3 install --no-cache-dir -U -r requirements.txt

CMD ["bash", "start"]
