import os
import tarfile
import pickle
import threading
import time

PICKLE_FILE = "students.pkl"
DATA_FILE = "students.dat"

class BackgroundPersistence:
    def __init__(self, method = "gz", debounce_sec = 0.3):
        self.method = method if method in ("gz", "none") else "gz"
        self.debounce_sec = debounce_sec
        self._lock = threading.Lock()
        self._event = threading.Event()
        self._stop = threading.Event()
        self._lastest_data = None
        self._thread = threading.Thread(target = self._worker, daemon = True)
        self._thread.start()
        
    def close(self, wait = True):
        self._stop.set()
        self._event.set()
        if wait:
            self._thread.join(timeout = 2)
            
    def notify_save(self, students, courses, marks):
        with self._lock:
            self._lastest_data = {"students": students, "courses": courses, "marks": marks}
        self._event.set()
        
    def _worker(self):
        while not self._stop.is_set():
            self._event.wait()
            self._event.clear()
            time.sleep(self.debounce_sec)
            with self._lock:
                data = self._lastest_data            
            if data is None:
                continue
            try:
                self._save_pickle(data)
                self._compress()
            except Exception:
                pass
    
    def _save_pickle(self, data):
        with open(PICKLE_FILE, "wb") as f:
            pickle.dump(data, f)
    
    def _compress(self):
        mod = "w:gz" if self.method == "gz" else "w"
        with tarfile.open(DATA_FILE, mod) as tar:
            if os.path.exists(PICKLE_FILE):
                tar.add(PICKLE_FILE, arcname = PICKLE_FILE)
                        
def dat_exists():
    return os.path.exists(DATA_FILE)

def decompress():
    with tarfile.open(DATA_FILE, "r:*") as tar:
        tar.extractall()
        
def load_pickle():
    if not os.path.exists(PICKLE_FILE):
        return [], [], []
    with open(PICKLE_FILE, "rb") as f:
        data = pickle.load(f)
    return data.get("students", []), data.get("courses", []), data.get("marks", [])


