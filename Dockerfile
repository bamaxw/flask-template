FROM python:3.7-slim
LABEL maintainer="max.wasylow@babylonhealth.com"


RUN groupadd -r appuser && useradd -u 1000 -r -g appuser appuser

RUN apt-get update \
    && apt-get install -y software-properties-common gcc libpq-dev python3-dev supervisor

ADD ./requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN pip3 install -r requirements.txt
RUN pip3 uninstall pip -y
ADD . /opt/app

ARG APP_NAME
ARG VENDOR
ARG DESCRIPTION
ARG GITHUB_URL
ARG BUILD_DATE
ARG VCS_REF
ARG SEMVER_VERSION

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=${BUILD_DATE}
LABEL org.label-schema.name=${APP_NAME}
LABEL org.label-schema.vendor=${VENDOR}
LABEL org.label-schema.description=${DESCRIPTION}
LABEL org.label-schema.vcs-url=${GITHUB_URL}
LABEL org.label-schema.vcs-ref=${VCS_REF}
LABEL org.label-schema.version=${SEMVER_VERSION}
LABEL org.label-schema.docker.cmd="docker run -p 8000:8000 -d ${APP_NAME}"

EXPOSE 8000

USER appuser
CMD ["bash", "run.sh", "--uwsgi"]

