#!/usr/bin/env bash

source .env
export APP_DB_DSN
make migrate-command
