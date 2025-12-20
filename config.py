# True açık demektir, False kapalı demektir.
# Varsayılan ayarlar parantez içinde yazılmıştır.

# -------------------------

# Dry run/test sürüşü açılsın mı? (False)
# True iken komutlar gerçekten çalıştırılmaz.
dry: bool = False

# Cockpit kurulumu yapılsın mı? (True)
cockpit: bool = True

# Çıktı sıkışık mı olsun? (True)
# True iken aralarda boşluk bırakılır.
compact: bool = True

# SSH servisinin adı ne? ("ssh")
# SSH servisi ile ilgili bir hata alırsanız bunu "ssh" yada "sshd" arasında değiştirmeyi deneyin.
ssh_service: str = "ssh"

# SSH drop-in config dosyasına ne yazılmalı?
ssh_config_content: str = """
PasswordAuthentication no
PubkeyAuthentication yes
"""

# SSH açık anahtarınız ne? ("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDNIljS9EpC44CkGvbcLd/iKIHmwOsgZFMAT2bVYBtzk bartin-lisesi")
ssh_public_key: str = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDNIljS9EpC44CkGvbcLd/iKIHmwOsgZFMAT2bVYBtzk bartin-lisesi"

# GRUB config dosyası nerede? ("/etc/default/grub")
grub_config_contents: str = "/etc/default/grub"

# GRUB drop-in config içine ne yazılmalı? (evet, biliyorum, ona tam olarak drop-in denmiyor, ama öyle gibi çalışıyor ve gerçekten de umrumda değil.)
grub_custom_conf: str = """GRUB_TIMEOUT=0
GRUB_TIMEOUT_STYLE=hidden
GRUB_TERMINAL=console
"""

# Dconf drop-in config dosyasına ne yazılmalı?
dconf_config_content: str = """[org/cinnamon/settings-daemon/plugins/power]
sleep-display-ac=10800
button-power='shutdown'
"""

# Dconf profil dosyasına ne yazılmalı?
profile_content: str = """user-db:user
system-db:local
"""

# Github repo ismi ne olmalı? ("siliconfire/bal-setup")
# Güncelleme için kullanılır. Bunu gerekmedikçe değiştirmeyin.
github_repo: str = "siliconfire/bal-setup"

# Branch adı ne? ("master")
# Güncelleme için kullanılır.
github_branch: str = "master"

# -------------------------

if __name__ == "__main__":
    print("Bu dosya doğrudan çalıştırılamaz. Lütfen main.py dosyasını çalıştırın.")
else:
    print("» Config dosyası yüklendi.")