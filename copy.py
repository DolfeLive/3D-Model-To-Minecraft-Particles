import pyperclip
import os
from pathlib import Path
import sys
from pynput import keyboard
import re
import signal
import threading

commands_dir = Path("./commands/")

if not commands_dir.exists():
    print("Path does not exist")
    sys.exit(0)
    


def wait_for_key(key_char):
    def on_press(key):
        try:
            if key.char == key_char:
                return False
        except AttributeError:
            pass
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

        
def numerical_sort(value):
    parts = re.split(r'(\d+)', str(value))
    parts[1::2] = map(int, parts[1::2])
    return parts
    
files = sorted(commands_dir.glob("command_*.txt"), key=numerical_sort)

print(f"Number of files found: {len(files)}")

for index, file in enumerate(files):
    print(f"Processing file {index + 1}/{len(files)}: {file}")
    with open(file, 'r') as txt:
        command = txt.read()
        pyperclip.copy(command)
        clipboard_content = pyperclip.paste()
        print(f"Copied content of {file} to clipboard: {clipboard_content[:30]}...")
        print("Press 'p' to continue to the next file...")
        wait_for_key('p')
        txt.close()

print("fin`")