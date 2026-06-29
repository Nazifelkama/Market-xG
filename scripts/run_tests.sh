#!/usr/bin/env bash
set -e

pytest
ruff check src tests
mypy src

