FROM tensorflow/tensorflow:2.6.0-gpu

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London
ENV INSTALL_DIR /orcanet

RUN apt-get update && apt-get install -y python3-tk python3-venv git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade --no-cache-dir pip setuptools wheel && pip install --no-cache-dir ipython
COPY . $INSTALL_DIR
# sed -i 's/tensorflow==/tensorflow-gpu==/' requirements.txt
RUN cd $INSTALL_DIR && make install
RUN cd / && rm -rf $INSTALL_DIR
