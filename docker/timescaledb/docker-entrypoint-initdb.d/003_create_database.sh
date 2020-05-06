#!/bin/bash

psql -U "${POSTGRES_USER}" postgres -c "CREATE DATABASE push_store;"
# psql -U "${POSTGRES_USER}" -d push_store -c "CREATE TABLE metrics(id BIGSERIAL NOT NULL PRIMARY KEY, uuid TEXT NOT NULL UNIQUE, title TEXT NOT NULL UNIQUE, status SMALLINT NOT NULL DEFAULT 1, datatype SMALLINT NOT NULL, description TEXT NOT NULL DEFAULT '', last_event TIMESTAMP WITHOUT TIME ZONE, ctime TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT timezone('utc', now()));"
