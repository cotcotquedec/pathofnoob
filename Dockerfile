FROM python:buster

# PACKAGE DE BASE
RUN apt update && apt install -y --no-install-recommends \
    build-essential git-all cmake

# COUCHBASE
RUN wget https://packages.couchbase.com/clients/c/repos/deb/couchbase.key \
    && apt-key add couchbase.key \
    && echo "deb https://packages.couchbase.com/clients/c/repos/deb/debian10 buster buster/main" >> /etc/apt/sources.list \
    && apt update \
    && apt install -y --no-install-recommends libcouchbase-dev libcouchbase3-tools

# DEBIAN PYTHON PACKAGE
RUN apt update && apt install -y --no-install-recommends \
    python3-pip python3-distutils-extra python3-dev python3-setuptools python3-scipy python3-numpy python3-matplotlib python3-pandas python3-sklearn

# PIP PACKAGE
RUN pip install scipy numpy matplotlib pandas sklearn requests

# PIP COUCHBASE
RUN pip install --pre couchbase

