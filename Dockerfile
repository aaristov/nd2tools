FROM python:latest
WORKDIR /root
COPY . .
RUN python -V &&\
    python setup.py install
CMD python -V && /bin/bash