#!/bin/bash
cd "$(dirname "$0")" 
xfce4-terminal --hold --color-text="#00BFFF" -e "bash -c 'source .venv/bin/activate && python3 main.py'"