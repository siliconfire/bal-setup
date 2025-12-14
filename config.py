# True açık demektir, False kapalı demektir.
# Varsayılan ayarlar parantez içinde yazılmıştır.

# -------------------------

# Dry run/test sürüşü açılsın mı? (False)
# True iken komutlar gerçekten çalıştırılmaz.
dry = True

# Cockpit kurulumu yapılsın mı? (True)
cockpit = True

# Çıktı sıkışık mı olsun? (True)
# True iken aralarda boşluk bırakılır.
compact = True

# SSH servisinin adı ne? ("ssh")
# SSH servisi ile ilgili bir hata alırsanız bunu "ssh" yada "sshd" arasında değiştirmeyi deneyin.
ssh_service = "ssh"

# SSH config dosyası nerede? ("/etc/ssh/sshd_config")
# Bunu gerekmedikçe değiştirmeyin.
ssh_config_path = "/etc/ssh/sshd_config"

# SSH açık anahtarınız ne? ("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDNIljS9EpC44CkGvbcLd/iKIHmwOsgZFMAT2bVYBtzk bartin-lisesi")
# Buradaki varsayılan anahtarın gizli anahtarını almak için beni okulda bulun (Çınar Mert Çeçen), yada cinar@cinarcecen.dev
ssh_public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDNIljS9EpC44CkGvbcLd/iKIHmwOsgZFMAT2bVYBtzk bartin-lisesi"

# GRUB config dosyası nerede? ("/etc/default/grub")
# Bunu gerekmedikçe değiştirmeyin.
grub_config_path = "/etc/default/grub"

# Github repo ismi ("siliconfire/bal-setup")
# Güncelleme için kullanılır. Bunu gerekmedikçe değiştirmeyin.
github_repo = "siliconfire/bal-setup"

# Branch adı ne? ("master")
# Güncelleme için kullanılır.
github_branch = "master"

# -------------------------

if __name__ == "__main__":
    print("Bu dosya doğrudan çalıştırılamaz. Lütfen main.py dosyasını çalıştırın.")
else:
    print("» Config dosyası yüklendi.")