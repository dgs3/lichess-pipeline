FROM python:3.7
WORKDIR /opt/conducto
ADD Makefile .
ADD requirements.txt .
ADD pipeline.py .
ADD scripts scripts/
RUN make venv
