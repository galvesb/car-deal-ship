#!/usr/bin/env bash

source .env
export APP_DB_DSN
make coverage-html-command
