#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "============================================================"
echo "🌾 GramSetu AI - Starting Application on Mac"
echo "============================================================"

# Check python3
if ! command -v python3 &> /dev/null
then
    echo "[!] python3 could not be found. Please install Python."
    exit 1
fi

export AUTO_OPEN=1
python3 server.py --open
