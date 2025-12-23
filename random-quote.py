#!/usr/bin/python
# Usage: python random-quote.py <highlights-file.json> [duration-seconds]
import os, sys
import argparse
import json
import random
import time
import subprocess
from datetime import datetime

# Argument parsing using argparse
parser = argparse.ArgumentParser(description='Display random quote from Kindle highlights JSON')
parser.add_argument('file', help='Path to highlights JSON file')
parser.add_argument('-d', '--duration', type=int, default=20, help='Display duration in seconds (screensaver mode)')
parser.add_argument('-s', '--screensaver', type=int, choices=[0,1], default=0, help='Run in screensaver mode (1) or show one quote and exit (0)')
parser.add_argument('-m', '--max-length', type=int,  help='Only select quotes with length less than MAX_LENGTH. If not set, full quotes are used.')
args = parser.parse_args()

if not os.path.exists(args.file):
    print("Invalid input json file")
    sys.exit(1)

# Assign parsed values
duration = args.duration
screensaver = args.screensaver
max_length = args.max_length

fp = open(args.file, 'r')
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
    
    # Calculate vertical positioning
    # If duration == 0 we are in single-quote mode: print at the top (no vertical padding)
    quote_lines = (len(quote) // (cols - 4)) + 1
    total_height = quote_lines + 3
    if duration == 0:
        # single-line, top-left aligned: combine and truncate to terminal width to avoid wrapping
        visible = f'"{quote}" -- From: {book}'
        if len(visible) > cols:
            visible = visible[:cols-3] + '...'
        sep = ' -- From: '
        sep_pos = visible.find(sep)
        if sep_pos != -1:
            quote_visible = visible[:sep_pos]
            book_visible = visible[sep_pos + len(sep):]
            print(f'{cyan}{bold}{quote_visible}{reset} {yellow}-- From: {book_visible}{reset}')
        else:
            print(f'{cyan}{bold}{visible}{reset}')
    else:
        top_padding = max(0, (lines - total_height) // 2)
        
        # Print empty lines for vertical centering
        for _ in range(top_padding):
            print()
        
        # Center and print quote
        print(quote_text.center(cols + len(cyan) + len(bold) + len(reset) - 3))
        print()
        print(book_text.rjust(cols - 4))
    
    # Log timestamp and how long this quote will display
    # print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Displaying for {duration}s")
    # sys.stdout.flush()
    
    # Display for specified duration
    time.sleep(duration)

def choose_quote(data, max_length):
    candidates = []
    for book, quotes in data.items():
        for q in quotes:
            if max_length is None or len(q) <= max_length:
                candidates.append((book, q))
    if not candidates:
        print("No quotes found matching criteria")
        sys.exit(1)
    return random.choice(candidates)


def show_one_quote_and_exit(data, cols, lines, max_length):
    book, quote = choose_quote(data, max_length)
    # Reuse the colored display function; duration=0 will print and return immediately
    display_quote_screensaver(quote, book, 0, cols, lines)
    sys.exit(0)

# If not running screensaver, show one colored quote and exit
if screensaver == 0:
    show_one_quote_and_exit(data, cols, lines, max_length) 

# Main screensaver loop
try:
    while True:
        book, quote = choose_quote(data, max_length)
        display_quote_screensaver(quote, book, duration, cols, lines)
except KeyboardInterrupt:
    #os.system('clear')
    print("Screensaver stopped")
    sys.exit(0)