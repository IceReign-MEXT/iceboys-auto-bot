#!/bin/bash
while true; do
    echo "Starting IceHub Tracker..."
    python3 ~/icehub_system/bot_main.py
    echo "Bot crashed or stopped. Restarting in 30s..."
    sleep 30
done
