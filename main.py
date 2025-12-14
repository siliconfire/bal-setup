"""
Ana kurulum scripti

-- Çınar Mert Çeçen <cinar@cinarcecen.dev>
-- Co-authored-by: Ali Efe Aktuğ <efealiaktug@gmail.com>
"""
import os
import sys

import config
import otokapat
import update
from utils import output, action, seperate, write_ssh_key


def main():
    if os.environ.get('WAS_UPDATED') == '1':
        print("\n\n\nGüncelleme başarılı. başlıyorum...")
        del os.environ['WAS_UPDATED']
    else:
        print(f"Kurulum scriptine hoş geldiniz!")

        if update.check_updates():
            output("Güncelleme varmış. Güncellemeyi yapalım...")
            update.main()
            os.environ['WAS_UPDATED'] = '1'
            os.execlp(sys.executable, sys.executable, *sys.argv)
        else:
            output("Güncelleme yok. başlıyorum...")
    seperate()

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

    action("ssh servisi başlatılıyor...", f"systemctl enable --now {config.ssh_service}")
    action("ssh için passwordauth kapatılıyor...", rf"""sed -i.bak -E 's/^[[:space:]]*#?\s*PasswordAuthentication\s*.*$/PasswordAuthentication no/g' {config.ssh_config_path}""")
    action("ssh için pubkeyauth açılıyor...", rf"""sed -i.bak -E 's/^[[:space:]]*#?\s*PubkeyAuthentication\s*.*$/PubkeyAuthentication yes/g' {config.ssh_config_path}""")
    action("ssh için gereken dosyalar oluşturuluyor...", "mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys", False)
    output("ssh için public key taşınıyor...")
    write_ssh_key()
    action("ssh servisi yeniden başlatılıyor...", f"systemctl restart {config.ssh_service}")
    seperate()

    action("grub-timeout 0 yapılıyor...", rf"""sed -i.bak -E 's/^[[:space:]]*#?\s*GRUB_TIMEOUT=.*$/GRUB_TIMEOUT=0/g' {config.grub_config_path}""")
    action("grub teması gizleniyor...", f"""grep -qxF 'GRUB_TIMEOUT_STYLE=hidden' {config.grub_config_path} || echo 'GRUB_TIMEOUT_STYLE=hidden' | sudo tee -a {config.grub_config_path} > /dev/null""")
    action("grub güncelleniyor...", "update-grub")
    seperate()

    output("Ali'nin otomatik kapatma servisinin kurulumu başlatılıyor...")
    otokapat.setup()


if "__main__" == __name__:
    main()
else:
    print("beni lütfen modül olarak kullanmayın.")

