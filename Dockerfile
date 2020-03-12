FROM python:buster

# ID FOR JUPYTER
ARG JH_ADMIN=pathofnoob
ARG JH_PWD=passofnoob

# PACKAGE DE BASE
RUN apt update && apt install -y --no-install-recommends \
    build-essential git-all cmake npm nodejs \
    && rm -rf /var/lib/apt/lists/*

# COUCHBASE
RUN wget https://packages.couchbase.com/clients/c/repos/deb/couchbase.key \
    && apt-key add couchbase.key \
    && echo "deb https://packages.couchbase.com/clients/c/repos/deb/debian10 buster buster/main" >> /etc/apt/sources.list \
    && apt update \
    && apt install -y --no-install-recommends libcouchbase-dev libcouchbase3-tools \
    && rm -rf /var/lib/apt/lists/*

# DEBIAN PYTHON PACKAGE
RUN apt update && apt install -y --no-install-recommends \
    python3-pip python3-distutils-extra python3-dev python3-setuptools python3-scipy python3-numpy python3-matplotlib \
    python3-pandas python3-sklearn  texlive-xetex texlive-fonts-recommended texlive-generic-recommended \
    && rm -rf /var/lib/apt/lists/*

# Jupyter
# Thank you to wawachief => https://github.com/wawachief/jupyterhubDocker
RUN npm install -g configurable-http-proxy \
    && pip install jupyterhub \
    && pip install --upgrade notebook \
    && pip install nbgrader nbconvert jupyterlab-server jupyter_contrib_nbextensions \
    && jupyter nbextension install --sys-prefix --py nbgrader --overwrite \
    && jupyter nbextension enable --sys-prefix --py nbgrader \
    && jupyter serverextension enable --sys-prefix --py nbgrader \
    && jupyter nbextension disable --sys-prefix formgrader/main --section=tree \
    && jupyter serverextension disable --sys-prefix nbgrader.server_extensions.formgrader

RUN groupadd admin \
    && useradd $JH_ADMIN -G admin --create-home --shell /bin/bash \
    && echo "$JH_ADMIN:$JH_PWD" | chpasswd \
    && mkdir -p /home/$JH_ADMIN/.jupyter \
    && mkdir /home/$JH_ADMIN/source


COPY docker/nbgrader_config.py /home/$JH_ADMIN/.jupyter/nbgrader_config.py
COPY docker/jupyterhub_config.py /srv/jupyterhub/

RUN chown -R $JH_ADMIN "/home/$JH_ADMIN" \
    && chmod 700 /home/$JH_ADMIN \
    && mkdir -p /srv/nbgrader/exchange \
    && chmod ugo+rw /srv/nbgrader/exchange \
    && mkdir /srv/feedback \
    && chmod 4777 /srv/feedback

RUN jupyter contrib nbextension install --sys-prefix

# PIP COUCHBASE
RUN pip install --pre couchbase

# PIP PACKAGE
RUN pip install scipy numpy matplotlib pandas sklearn requests

EXPOSE 8000
EXPOSE 8001
CMD ["jupyterhub"]


