FROM python:latest
WORKDIR /root
COPY . .
RUN python -V &&\
    python -m pip install -r requirements.txt &&\
    python setup.py install
CMD python -V && jupyter lab