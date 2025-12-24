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
    print("""
[»] | Çınar Mert Çeçen <cinar@cinarcecen.dev>
    | Ali Efe Aktuğ <efealiaktug@gmail.com>
    | github: siliconfire/bal-setup
""")

    if os.environ.get('WAS_UPDATED') == '1':
        print("\n\n\nGüncelleme başarılı. başlıyorum...")
        del os.environ['WAS_UPDATED']
    else:
        output(f"Kurulum scriptine hoş geldiniz!")

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

    # fikir: kalgebra kgeography kalzium kstars
    action("apt üzerinden program kuruluyor...", "apt install helix vim openssh-server flatpak gnome-software-plugin-flatpak dconf-cli okular openboard xournalpp geogebra -y")
    seperate()

    action("flatpak depoları ekleniyor...", "flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo", sudo=False)
    seperate()

    # fikir:
    action("flatpak üzerinden program kuruluyor...", "flatpak install flathub com.github.flxzt.rnote se.sjoerd.Graphs -y")

    if config.cockpit:
        action("cockpit kuruluyor...", "apt install cockpit -y")
        action("cockpit servisi başlatılıyor...", "systemctl enable --now cockpit.socket")
    else:
        print("[!] | cockpit kurulumu atlandı.\n    | bunu değiştirmek için config.py dosyasına müracaat edebilirsiniz.")
    seperate()

    action("ssh servisi başlatılıyor...", f"systemctl enable --now {config.ssh_service}")
    action("ssh custom config oluşturuluyor...", f"echo '{config.ssh_config_content}' | sudo tee /etc/ssh/sshd_config.d/99-custom.conf > /dev/null", shell=True)
    action("ssh için gereken dosyalar oluşturuluyor...", "mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys", sudo=False, shell=True)
    output("ssh için public key taşınıyor...")
    write_ssh_key()
    action("ssh servisi yeniden başlatılıyor...", f"systemctl restart {config.ssh_service}")
    seperate()

    action("grub ayarları (timeout ve tema) güncelleniyor...", f"echo '{config.grub_config_content}' | sudo tee /etc/default/grub.d/99-custom.cfg > /dev/null", shell=True)
    action("grub güncelleniyor...", "update-grub")
    seperate()

    action("dconf profil dosyası oluşturuluyor...", f"mkdir -p /etc/dconf/profile && echo '{config.profile_content}' | sudo tee /etc/dconf/profile/user > /dev/null", shell=True)
    action("dconf yerel veritabanı dizini oluşturuluyor...", "mkdir -p /etc/dconf/db/local.d/", shell=True)
    action("dconf config dosyası yazılıyor...", f'echo "{config.dconf_config_content}" | sudo tee /etc/dconf/db/local.d/00-power > /dev/null', shell=True)
    action("dconf veritabanı güncelleniyor...", "dconf update")
    seperate()

    action("Sudo config dosyası atılıyor...", f"echo '{config.sudo_config_content}' | sudo tee /etc/sudoers.d/99-options > /dev/null", shell=True)
    action("Sudo config dosyasının yetkileri düzenleniyor...", "sudo chmod 0440 /etc/sudoers.d/99-options", shell=True)
    seperate()

    output("Ali'nin otomatik kapatma servisinin kurulumu başlatılıyor...")
    otokapat.setup()
    seperate()

    print("""
    
[+] | işim bitti gibi görünüyor. bir sonraki adımlar:
    | 1. Ayarlar » Tercih edilen uygulamalar » Video = VLC, PDF = Okular
    | 2. Openboard'ı görev çubuğuna ve masaüstüne sabitle
    | 3. biraz sıvı iç. ben su tercih ediyorum.
    
[»] | Çınar Mert Çeçen <cinar@cinarcecen.dev>
    | Ali Efe Aktuğ <efealiaktug@gmail.com>
    | github: siliconfire/bal-setup
    
""")
    output("kolay gelsin. kapatıyorum burada, görüşürüz.")

if "__main__" == __name__:
    main()
else:
    print("beni lütfen modül olarak kullanmayın.")
