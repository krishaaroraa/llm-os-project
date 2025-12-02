import os
import subprocess
import threading
import time
import sys
from model_utils import load_model, generate_response
from collections import deque

# Folders
READY_FOLDER = "ready_files"
RUNNING_FOLDER = "running_files"
FINISHED_FOLDER = "finished_files"

# Initialize folders if not exist
for folder in [READY_FOLDER, RUNNING_FOLDER, FINISHED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Queue for scheduling (FCFS)
ready_queue = deque()

# Track files
loading_done = False

def typewriter(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def loading_animation():
    boot_frames = [
        "[BOOT] Initializing core modules.",
        "[BOOT] Checking GPU backend...",
        "[BOOT] Optimizing tokenizer...",
        "[BOOT] Compiling neural layers...",
        "[BOOT] Patching transformer heads...",
        "[BOOT] Installing Felix personality module...",
        "[BOOT] Activating code-generation protocols...",
        "[BOOT] Establishing connection to AI consciousness...",
        "[BOOT] Felix core online.",
        "[✓] Ready for interaction."
    ]
    print("\033c", end="")  # Clear screen
    print(r"""
 ________        .__       .__           _________.__       .__
/  _____/  ____  |__| ____ |  |__  ______\__    ___|__| ____ |  |__
\   \  ___ /  _ \ |  |/ __ \|  |  \ \____ \|    |  |  |/ __ \|  |  \
 \    \_\  (  <_> )|  \  ___/|   Y  \|  |_> >    |  |  \  ___/|   Y  \
  \______  /\____/ |__|\___  >___|  /|   __/|____|  |__|\___  >___|  /
         \/                 \/     \/ |__|                    \/     """)
    print("\n[FelixOS AI Terminal v1.0]")
    print("──────────────────────────────────────────────\n")
    time.sleep(1)

    for line in boot_frames:
        if loading_done:
            break
        typewriter(line)
        time.sleep(0.3)

    if not loading_done:
        time.sleep(0.5)
        print("\nLaunching Felix...\n")
        time.sleep(0.5)
    else:
        print("\n⏹ Boot interrupted.")


def save_script_to_file(script_content, file_name):
    file_path = os.path.join(READY_FOLDER, file_name)
    with open(file_path, 'w') as file:
        file.write(script_content)
    print(f"✅ Saved script to {file_path}")
    return file_path


def move_file_to_running(file_name):
    src = os.path.join(READY_FOLDER, file_name)
    dest = os.path.join(RUNNING_FOLDER, file_name)
    os.rename(src, dest)
    print(f"✅ Moved {file_name} to running files.")


def move_file_to_finished(file_name):
    src = os.path.join(RUNNING_FOLDER, file_name)
    dest = os.path.join(FINISHED_FOLDER, file_name)
    os.rename(src, dest)
    print(f"✅ Moved {file_name} to finished files.")


def run_script(file_name):
    script_path = os.path.join(RUNNING_FOLDER, file_name)
    subprocess.run(f"bash {script_path}", shell=True)
    move_file_to_finished(file_name)


def fcfs_scheduling():
    """First-Come, First-Served scheduling"""
    if ready_queue:
        file_name = ready_queue.popleft()  # Take the first file in the queue
        move_file_to_running(file_name)
        run_script(file_name) 


def main():
    while True:
        try:
            command = input("$> ").strip()

            if command.lower() in ['exit', 'quit']:
                print("Exiting shell.")
                break

            if not command:
                continue

            if command.startswith('cd '):
                path = command[3:].strip()
                try:
                    os.chdir(path)
                except FileNotFoundError:
                    print(f"No such directory: {path}")
                continue

            if command.startswith('felix '):
                user_input = command[6:].strip()
                static_instruction = (
                    "You are a helpful coding assistant. "
                    "Generate a complete and correct bash script as a `.sh` file. "
                    "The output must be runnable in a Unix shell. "
                    "Do not explain — only provide the bash code.\n\n"
                    f"User request: {user_input}"
                )

                print("\n🤖 Felix is thinking...\n")
                script_content = generate_response(gen, static_instruction)
                
                # Save the generated script to the 'ready files' folder
                file_name = f"script_{int(time.time())}.sh"
                script_path = save_script_to_file(script_content, file_name)

                # Add to the ready queue
                ready_queue.append(file_name)

                # Call the scheduling algorithm to handle the ready queue
                fcfs_scheduling()
                
                continue

            subprocess.run(command, shell=True)

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt. Type 'exit' to quit.")
        except EOFError:
            print("\nEOF received. Exiting shell.")
            break


if __name__ == "__main__":

    # Start animation thread
    spinner_thread = threading.Thread(target=loading_animation)
    spinner_thread.start()

    # Load model
    gen = load_model('deepseek')

    # Stop animation and join thread
    loading_done = True
    spinner_thread.join()

    print("✅ Felix is fully loaded. Use 'felix <your prompt>' to begin.\n")
    main()
