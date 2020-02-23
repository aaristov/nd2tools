FROM continuumio/miniconda3
WORKDIR /root
COPY . .
# RUN apt-get update &&\
#     apt-get install gcc -y &&\
#     apt-get install libtiff-dev -y &&\
    # conda update -n base -c defaults conda &&\
    # conda install libtiff libgcc -y &&\
    # python -m pip install --upgrade pip setuptools &&\
# RUN python -m pip install numpy &&\
    # python -m pip install libtiff &&\
RUN python -m pip install -r requirements.txt
    # python -m pytest
CMD /bin/bash