#!/usr/bin/env python3
# A simple command-line timer that sends a desktop notification when time is up.

import time
import sys
import subprocess

def notify(title, message):
    # Using subprocess is more robust than os.system
    subprocess.run(["notify-send", title, message])

def start_timer():
    try:
        # Get minutes from the command line, default to 5 (Pomodoro)
        minutes = float(sys.argv[1]) if len(sys.argv) > 1 else 5
        # Get custom message or use default
        label = sys.argv[2] if len(sys.argv) > 2 else "Time's up!"
        
        print(f"Timer set for {minutes} minutes: [{label}]")
        time.sleep(minutes * 60)
        notify("Timer Finished", label)
        
    except ValueError:
        print("Usage: timer [minutes] ['message']")
    except KeyboardInterrupt:
        print("\nTimer cancelled.")

if __name__ == "__main__":
    start_timer()