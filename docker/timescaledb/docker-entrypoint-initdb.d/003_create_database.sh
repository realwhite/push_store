#!/bin/bash

psql -U "${POSTGRES_USER}" postgres -c "CREATE DATABASE push_store;"
