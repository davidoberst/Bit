#!/bin/bash
cd "$(dirname "$0")" #ubicarse ne directorio actual
xfce4-terminal --hold -e "bash -c 'source .venv/bin/activate && python3 main.py'"