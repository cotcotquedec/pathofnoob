FROM python:buster

# DEBIAN PYTHON PACKAGE
RUN apt update && apt install -y --no-install-recommends \
    python3-pip python3-distutils-extra python3-dev python3-scipy python3-numpy python3-matplotlib python3-pandas python3-sklearn

# PIP PACKAGE
RUN pip install scipy numpy matplotlib pandas sklearn requests