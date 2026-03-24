from pathlib import Path
import subprocess

def normalize_mp3_folder(folder_path, target_db=-18.0, album_mode=False, recursive=False):
    root = Path(folder_path).expanduser()
    if not root.exists():
        print(f"Folder does not exist: {root}")
        return
    if not root.is_dir():
        print(f"Not a folder: {root}")
        return
    candidates = root.rglob("*.mp3") if recursive else root.glob("*.mp3")
    files = sorted(p for p in candidates if p.is_file())
    if not files:
        print("No mp3 files found in the folder.")
        return
    print(f"Found {len(files)} mp3 files.")
    gain_db = 89 + target_db
    cmd = ["mp3gain", "-q", "-r"]
    if album_mode:
        cmd.append("-a")
    cmd.extend(["-d", str(int(gain_db * 10))])
    paths = [str(p) for p in files]
    try:
        result = subprocess.run(cmd + paths, capture_output=True, text=True, check=True)
        print("ReplayGain applied successfully.")
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("mp3gain failed:")
        print(e.stderr)

if __name__ == "__main__":
    print("Install: sudo apt install mp3gain")
    folder = input("Input folder: ").strip()
    normalize_mp3_folder(folder, album_mode=False)

