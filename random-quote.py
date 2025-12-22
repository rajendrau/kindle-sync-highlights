#!/usr/bin/python
# Usage: python random-quote.py <highlights-file.json> [duration-seconds]
import os, sys
import json
import random
import time
import subprocess

if len(sys.argv) < 2:
    print("Usage: python random-quote.py <highlights-file.json> [duration-seconds]")
    sys.exit(1)

if not os.path.exists(sys.argv[1]):
    print("Invalid input json file")
    sys.exit(1)

# Get duration from argument (default 20 seconds)
duration = 20
if len(sys.argv) > 2:
    try:
        duration = int(sys.argv[2])
    except ValueError:
        print("Duration must be an integer")
        sys.exit(1)
    
fp = open(sys.argv[1], 'r')
data = json.load(fp)

# Get terminal dimensions for centering
result = subprocess.run(['tput', 'cols'], capture_output=True, text=True)
cols = int(result.stdout.strip()) if result.returncode == 0 else 80
result = subprocess.run(['tput', 'lines'], capture_output=True, text=True)
lines = int(result.stdout.strip()) if result.returncode == 0 else 24

def display_quote_screensaver(quote, book, duration, cols, lines):
    # Clear screen
    os.system('clear')
    
    # ANSI color codes
    cyan = '\033[36m'
    yellow = '\033[33m'
    reset = '\033[0m'
    bold = '\033[1m'
    
    # Prepare text
    quote_text = f'{cyan}{bold}"{quote}"{reset}'
    book_text = f'{yellow}-- From: {book}{reset}'
    
    # Calculate vertical centering
    quote_lines = (len(quote) // (cols - 4)) + 1
    total_height = quote_lines + 3
    top_padding = max(0, (lines - total_height) // 2)
    
    # Print empty lines for vertical centering
    for _ in range(top_padding):
        print()
    
    # Center and print quote
    print(quote_text.center(cols + len(cyan) + len(bold) + len(reset) - 3))
    print()
    print(book_text.rjust(cols - 4))
    
    # Display for specified duration
    time.sleep(duration)

# Main screensaver loop
try:
    while True:
        ind = random.randint(0, len(data) - 1)
        book = list(data.keys())[ind]
        quote = random.choice(data[book])
        display_quote_screensaver(quote, book, duration, cols, lines)
except KeyboardInterrupt:
    os.system('clear')
    print("Screensaver stopped")
    sys.exit(0)