#!/bin/bash
>&2 echo "add ' | bash' to execute rm  in shell - after checking following output"

find . -type d -name __pycache__ -printf "rm -r %p\n"
find . -type d -name \\.mypy_cache -printf "rm -r %p\n"
find . -type d -name \\.ruff_cache -printf "rm -r %p\n"
