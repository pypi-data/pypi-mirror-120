
FROM ubuntu:bionic
LABEL maintainer="Shyam Sudhakaran <shyamsnair97@gmail.com>"                                           

ENV                                    \
  DEBIAN_FRONTEND=noninteractive                                       \
  LANG=C.UTF-8                                                         \
  LC_ALL=C.UTF-8                                                       \
  PATH=/opt/conda/bin:$PATH                                            \
TZ=America/Los_Angeles     

# Install system packages.
RUN apt-get update       \
  && apt-get install -y  \
    build-essential      \
    bzip2                \
    ca-certificates      \
    curl                 \
    git                  \
    tzdata               \
    wget                 \
    gcc                  \
    libgl1-mesa-glx      \
  && apt-get clean       \
  && apt-get autoremove  \
  && rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc

RUN conda create -n env -y python=3.8.0
RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

ADD pre-install-setup.sh /usr/local/bin/pre-install-setup.sh
RUN chmod 777 /usr/local/bin/pre-install-setup.sh
RUN /usr/local/bin/pre-install-setup.sh

ENV CODE_ROOT /code/power_cogs

RUN mkdir -p $CODE_ROOT
COPY . $CODE_ROOT
WORKDIR $CODE_ROOT

RUN python setup.py install

ADD post-install-setup.sh /usr/local/bin/post-install-setup.sh
RUN chmod 777 /usr/local/bin/post-install-setup.sh
RUN /usr/local/bin/post-install-setup.sh

ADD run-ray.sh /usr/local/bin/run-ray.sh
RUN chmod 777 /usr/local/bin/run-ray.sh