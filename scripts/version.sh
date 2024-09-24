#!/bin/bash


if [ -z "${VERSION}" ]; then
  echo "VERSION is not set. Please set the VERSION environment variable."
  exit 1
fi

ls -al

sed  -i '' -e "s/^version =.*/version = \"${VERSION}\"/" pyproject.toml
sed  -i '' -e "s/^__version__ =.*/__version__ = \"${VERSION}\"/" reattempt/__init__.py