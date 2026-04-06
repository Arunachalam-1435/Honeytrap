#!/bin/bash

echo "Starting SSH Honeypot..."
python3 honeytrap.py -a 0.0.0.0 -p 2222 --ssh &

echo "Starting Web Hoenypot..."
python3 honeytrap.py -a 0.0.0.0 -p 8080 --web &

wait