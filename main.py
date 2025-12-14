"""
Ana kurulum scripti

-- Çınar Mert Çeçen <cinar@cinarcecen.dev>
-- Co-authored-by: Ali Efe Aktuğ <efealiaktug@gmail.com>
"""

import subprocess
import time
import os

from utils import run, output, action, seperate
import otokapat
import config


def main():
    print(f"Kurulum scriptine hoş geldiniz! (versiyon {config.ver})")

    action("apt güncellemeleri çekiliyor...", "apt update -y")
    action("apt güncellemeleri kuruluyor...", "apt upgrade -y")
    action("apt autoremove...", "apt autoremove -y")
    seperate()

    action("apt üzerinden program kuruluyor...", "apt install helix vim openssh-server flatpak gnome-software-plugin-flatpak openboard -y")
    seperate()

    action("flatpak depoları ekleniyor...", "flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo", False)
    seperate()

    if config.cockpit:
        action("cockpit kuruluyor...", "apt install cockpit -y")
        action("cockpit servisi başlatılıyor...", "systemctl enable --now cockpit.socket")
        seperate()

    action("ssh servisi aktifleştiriliyor...", f"systemctl enable --now {config.ssh_service}")
    action("ssh servisi başlatılıyor...", f"systemctl start {config.ssh_service}")
    action("ssh için passwordauth kapatılıyor...", f"""sed -i.bak -E 's/^[[:space:]]*#?[[:space:]]*PasswordAuthentication.*/PasswordAuthentication no/g' {config.ssh_config_path}""")
    action("ssh için pubkeyauth açılıyor...", f"""sed -i.bak -E 's/^[[:space:]]*#?[[:space:]]*PubkeyAuthentication.*/PubkeyAuthentication yes/g' {config.ssh_config_path}""")
    action("ssh için gereken dosyalar oluşturuluyor...", "mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys")
    action("ssh için public key taşınıyor...", f"echo '{config.ssh_public_key}' >> ~/.ssh/authorized_keys")
    action("ssh servisi yeniden başlatılıyor...", f"systemctl restart {config.ssh_service}")
    seperate()

    action("grub-timeout 0 yapılıyor...", f"""sed -i.bak -E 's/^[[:space:]]*#?[[:space:]]*GRUB_TIMEOUT=.*/GRUB_TIMEOUT=0/g' {config.grub_config_path}""")
    action("grub teması gizleniyor...", f"echo 'GRUB_TIMEOUT_STYLE=hidden' | sudo tee -a {config.grub_config_path} > /dev/null")
    action("grub güncelleniyor...", "update-grub")
    seperate()

    output("Ali'nin otomatik kapatma servisinin kurulumu başlatılıyor...")
    otokapat.setup()

if "__main__" == __name__:
    main()
else:
    print("beni lütfen modül olarak kullanmayın.")

