from pathlib import Path
from rgain3 import ReplayGain

def normalize_mp3_folder(folder_path, target_db=-18.0, album_mode=False, recursive=False):
    root = Path(folder_path).expanduser()
    if not root.exists():
        raise FileNotFoundError(f"Folder does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a folder: {root}")
    candidates = root.rglob("*") if recursive else root.iterdir()
    files = sorted(p for p in candidates if p.is_file() and p.suffix.lower() == ".mp3")
    if not files:
        print("No mp3 files found in the folder.")
        return
    rg = ReplayGain()
    paths = [str(p) for p in files]
    if album_mode:
        print(f"Calculating album gain for {len(files)} files...")
        try:
            gain_data = rg.calculate_album_gain(paths, target_db)
        except Exception as exc:
            raise RuntimeError(f"Album gain calculation failed: {exc}") from exc
        failures = 0
        for path in paths:
            try:
                rg.write_gain(path, gain_data)
            except Exception as exc:
                failures += 1
                print(f"Failed to write gain for {path}: {exc}")
        if failures:
            print(f"Finished with {failures} write failures.")
        else:
            print("Finished applying ReplayGain tags.")
        return
    print(f"Calculating track gain for {len(files)} files...")
    failures = 0
    for path in paths:
        try:
            gain_data = rg.calculate_track_gain(path, target_db)
            rg.write_gain(path, gain_data)
        except Exception as exc:
            failures += 1
            print(f"Failed for {path}: {exc}")
    if failures:
        print(f"Finished with {failures} failures.")
    else:
        print("Finished applying ReplayGain tags.")

if __name__ == "__main__":
    folder = input("Input folder: ").strip()
    normalize_mp3_folder(folder, album_mode=False)

