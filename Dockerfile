FROM alpine:3.11

RUN apk add --update python3 py3-cffi py3-cryptography py3-netifaces
RUN python3 -m venv --system-site-packages /venv
COPY . /src
RUN . /venv/bin/activate; \
	cd /src; \
	pip install -e .

ENTRYPOINT ["/venv/bin/nova-exporter"]
