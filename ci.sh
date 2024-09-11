#! /bin/bash -ex
COV_ARGS=""

if [ -n "$HTMLCOV" ]; then
  COV_ARGS="$COV_ARGS --cov-report=html"
fi
if [ -n "$BRANCHCOV" ]; then
  COV_ARGS="$COV_ARGS --cov-branch"
fi


poetry run mypy --check-untyped-defs --explicit-package-bases trengo

if [ -n "$CI_MYPY_ONLY" ]; then
  exit 0
fi

# poetry run pytest --cov=. $COV_ARGS tests/
