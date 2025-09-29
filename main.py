import subprocess
import time
import os

# Render deploy sẽ chạy trong thư mục làm việc mặc định
BASE_DIR = os.getcwd()
XMRIG_PATH = os.path.join(BASE_DIR, "xmrig-6.24.0/xmrig")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

THREADS = 4  # ví dụ muốn giới hạn CPU

def run_xmrig():
    cmd = [XMRIG_PATH, "-c", CONFIG_PATH]
    if THREADS:
        cmd += ["--threads", str(THREADS)]
    print(">>> Starting xmrig:", " ".join(cmd), flush=True)

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        for line in proc.stdout:
            print(line, end="", flush=True)
    except Exception as e:
        print("Error reading output:", e, flush=True)
    finally:
        proc.wait()
        return proc.returncode

if __name__ == "__main__":
    # đảm bảo binary có quyền chạy
    try:
        os.chmod(XMRIG_PATH, 0o755)
    except Exception:
        pass

    while True:
        rc = run_xmrig()
        print(f">>> xmrig exited with code {rc}, restarting in 5s...", flush=True)
        time.sleep(5)
