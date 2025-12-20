import subprocess
import time
import os
from pathlib import Path

import config

def run(command: str, sudo: bool = True):
    if sudo:
        command = "sudo -S " + command
    if config.dry:
        time.sleep(0.2)
        # print(f"[DRY RUN] {command}")
        return
    command = command.split()
    subprocess.run(command)


def output(message: str):
    print(f"[!] {message}")

def output2(message: str):
    print(f"| {message}")


def action(message: str, command: str, sudo: bool = True):
    if not config.compact:
        print()
    output(message)
    run(command, sudo)

def action2(message: str, command: str, sudo: bool = True):
    if not config.compact:
        print()
    output2(message)
    run(command, sudo)

def seperate():
    print("\n" + "-"*20 + "\n")

def write_ssh_key(use_root: bool = False):
    if use_root:
        ssh_dir = Path("/root/.ssh")
    else:
        # eğer sudo isek Path.home() root da olabilir o yüzden kendimiz bulalım
        # valla olmayadabilir bilmiyorum aslında, riski almak isteyen varsa PR atabilir vaktim yok
        user = os.environ.get("SUDO_USER") or os.getlogin()
        ssh_dir = Path(f"/home/{user}/.ssh")

    ssh_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    file_path = ssh_dir / "authorized_keys"

    with file_path.open("a") as f:
        f.write(f"\n{config.ssh_public_key}\n")

    # yetkilerden emin olalım, ben bile ssh kadar seçici değilim abi (kola içmiyorum)
    os.chmod(file_path, 0o600)
    os.chmod(ssh_dir, 0o700)


if __name__ == "__main__":
    print("Bu dosya doğrudan çalıştırılamaz. Lütfen main.py dosyasını çalıştırın.")