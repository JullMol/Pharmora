import subprocess
import sys
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_DIR = "."
ENTRY_SCRIPT = "gui/pharmora_gui.py"
DEBOUNCE_SECONDS = 8

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.timer = None
        self.lock = threading.Lock()
        self.restart()

    def restart(self):
        with self.lock:
            if self.process:
                print("🛑 Stopping old process...")
                self.process.terminate()
            print(f"▶️  Starting {ENTRY_SCRIPT}")
            self.process = subprocess.Popen([sys.executable, ENTRY_SCRIPT])

    def schedule_restart(self):
        with self.lock:
            if self.timer:
                self.timer.cancel()
            print(f"⏳ Waiting {DEBOUNCE_SECONDS}s to restart...")

            self.timer = threading.Timer(DEBOUNCE_SECONDS, self.restart)
            self.timer.daemon = True
            self.timer.start()

    def on_modified(self, event):
        if event.src_path.endswith((".py", ".kv")):
            print(f"📝 Change detected: {event.src_path}")
            self.schedule_restart()

if __name__ == "__main__":
    handler = ReloadHandler()
    observer = Observer()
    observer.schedule(handler, path=WATCHED_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        if handler.process:
            handler.process.terminate()
    observer.join()