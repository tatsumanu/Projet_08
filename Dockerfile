FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    supervisor \
    nginx \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY nginx_purbeurre /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx_purbeurre /etc/nginx/sites-enabled
COPY projet_08-gunicorn.conf /etc/supervisor/conf.d/

