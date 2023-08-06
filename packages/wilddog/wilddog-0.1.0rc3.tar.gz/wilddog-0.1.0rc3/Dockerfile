FROM python:3.9-slim as build

RUN apt-get update && apt-get install -y --no-install-recommends git libpq5 gcc libpq-dev python-dev

COPY . /wilddog
WORKDIR /wilddog

RUN pip install .

FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends libpq5

COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin/wilddog /usr/local/bin/wilddog
COPY --from=build /wilddog/wilddog.toml /opt/wilddog/wilddog.toml

WORKDIR /opt/wilddog
CMD wilddog start
