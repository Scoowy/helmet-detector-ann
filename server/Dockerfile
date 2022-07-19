# FROM quay.io/opencv-ci/opencv-python-manylinux2014-x86-64:20220628
FROM python:3.10.4-alpine

WORKDIR /app

ENV FLASK_APP server.py
ENV FLASK_ENV production
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8000

# RUN apk add --no-cache gcc musl-dev linux-headers

RUN apk update \
    && apk add --upgrade --no-cache \
    bash openssh curl ca-certificates openssl less htop \
    g++ make wget rsync gcc linux-headers \
    build-base libpng-dev freetype-dev libexecinfo-dev openblas-dev libgomp lapack-dev \
    libgcc libquadmath musl  \
    libgfortran \
    lapack-dev \
    &&  pip install --no-cache-dir --upgrade pip

RUN pip install --upgrade setuptools wheel

RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip install opencv-python-headless

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "server.py"]
