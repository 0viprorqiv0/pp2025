import os
import tarfile
import pickle
PICKLE_FILE = "students.pkl"
DATA_FILE = "students.dat"

def dat_exists():
    return os.path.exists(DATA_FILE)

def save_pickle(students, courses, marks):
        data = {"students": students, "courses": courses, "marks": marks}
        with open(PICKLE_FILE, "wb") as f:
            pickle.dump(data, f)
            
def load_pickle():
    if not os.path.exists(PICKLE_FILE):
        return [], [], []
    with open(PICKLE_FILE, "rb") as f:
        data = pickle.load(f)
    return data.get("students, []"), data.get("courses, []"), data.get("marks", [])

def compress(method = "gz"):
    mode = "w:gz" if method == "gz" else "w"
    with tarfile.open(DATA_FILE, mode) as tar:
        if os.path.exists(PICKLE_FILE):
            tar.add(PICKLE_FILE, arcname = PICKLE_FILE)

def decompress():
    with tarfile.open(DATA_FILE, "r:*") as tar:
        tar.extractall()
        
        