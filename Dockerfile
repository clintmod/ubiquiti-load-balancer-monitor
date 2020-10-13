FROM python:alpine as base

RUN apk add --update --no-cache --purge bash curl openssh-client sshpass \
  && rm -rf /var/cache/apk/* /tmp/*

RUN sed -i 's#/root:/bin/ash#/root:/bin/bash#g' /etc/passwd

WORKDIR /opt/ubiquiti-monitor

ENV APP_HOME=/opt/ubiquiti-monitor

FROM base as compile

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="/root/.poetry/bin:${PATH}"

COPY pyproject.toml poetry.lock .

RUN touch README.md && \
  mkdir -p src/ubiquiti_monitor && \
  touch src/ubiquiti_monitor/__init__.py

RUN poetry config virtualenvs.in-project true

RUN poetry install

FROM base as final

COPY . .

COPY --from=compile /opt/ubiquiti-monitor/.venv/ /opt/ubiquiti-monitor/.venv/

ENV PATH="$APP_HOME/.venv/bin:${PATH}"
ENV VIRTUAL_ENV=$APP_HOME/.venv

# RUN pytest

CMD ubiquiti-monitor
