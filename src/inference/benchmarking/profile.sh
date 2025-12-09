#!/bin/bash

SCRIPT=$1
OUT="${SCRIPT%.py}.prof"

echo "Profilling $SCRIPT"
python "$SCRIPT"

snakeviz "$OUT"