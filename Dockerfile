FROM ubuntu:18.04

RUN apt-get update -y \
	&& apt-get install -y python3-pip python3-dev \
	&& rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install flask flask_json

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"

EXPOSE 8866

COPY ./ ./
CMD ["python3", "serve.py"]
