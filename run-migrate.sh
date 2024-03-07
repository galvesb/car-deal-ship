#!/bin/bash
set -e

[[ $DEBUG ]] && set -x

exec mongodb-migrate --url $APP_DB_DSN --migrations migrations