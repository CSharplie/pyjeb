#!/usr/bin/env bash
set -euo pipefail

echo "[post-create] Installing Git LFS"
sudo apt-get update
sudo apt-get install -y git-lfs

echo "[post-create] Initializing Git LFS"
git lfs install

echo "[post-create] Installing Python tooling"
pip install pytest pylint pre-commit

echo "[post-create] Installing pre-commit hooks"
pre-commit install

echo "[post-create] Done"
