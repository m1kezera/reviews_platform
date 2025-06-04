import subprocess
import time
import os

# Caminhos absolutos dos watchdogs
WATCHDOG_CLEANER = "watchdogs/watchdog_input_cleaner.py"
WATCHDOG_PIPELINE = "watchdogs/pipeline_watchdog.py"

def start_watchdog(script_path):
    return subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    print("🚀 Starting Watchdogs...")

    # Inicia os dois watchdogs em janelas separadas
    cleaner_process = start_watchdog(WATCHDOG_CLEANER)
    time.sleep(1)
    pipeline_process = start_watchdog(WATCHDOG_PIPELINE)

    print("✅ Watchdogs running:")
    print(f" - Input Cleaner: PID {cleaner_process.pid}")
    print(f" - Pipeline Processor: PID {pipeline_process.pid}")

    print("⏹️ Press Ctrl+C to stop both (you may need to close each window manually).")
    try:
        cleaner_process.wait()
        pipeline_process.wait()
    except KeyboardInterrupt:
        cleaner_process.terminate()
        pipeline_process.terminate()
        print("\n⛔ Watchdogs stopped.")
