#!/bin/bash
set -euo pipefail

uv sync
uv run uvicorn main:app --reload
