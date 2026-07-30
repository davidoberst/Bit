#!/bin/bash
cd "$(dirname "$0")"

desktop="$XDG_CURRENT_DESKTOP"

if [ "$desktop" = "XFCE" ]; then
    xfce4-terminal --hold --color-text="#f7f7f7" --color-bg="#000000" -e "bash -c 'source .venv/bin/activate && python3 main.py'"
elif [ "$desktop" = "KDE" ]; then
    konsole --noclose -e bash -c 'source .venv/bin/activate && python3 main.py'
fi