import subprocess
import time
import os

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


def write_ssh_key():
    path = os.path.expanduser("~/.ssh/authorized_keys")
    with open(path, 'a') as f:
        f.write(config.ssh_public_key + '\n')


if __name__ == "__main__":
    print("Bu dosya doğrudan çalıştırılamaz. Lütfen main.py dosyasını çalıştırın.")