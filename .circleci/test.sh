#!/usr/bin/env bash

set -e
set -o pipefail

SERVICE="${1:?## Err: Please specify the service}"

echo "Running tests for $SERVICE..."
# Add "set -x" to the below to see the lists of files being tested.
docker-compose run --rm $SERVICE sh -c "\
    echo \"🔬  Running pytest tests…\" && \
    pytest --exitfirst --cov --cov-report=xml:tests/coverage.xml && \
    echo \"🔍  Reporting on code coverage…\" && \
    coverage report --show-missing"
echo "👌  OK!"