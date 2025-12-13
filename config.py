# True açık demektir, False kapalı demektir.
# Varsayılan ayarlar parantez içinde yazılmıştır.
ver = 1   # Bunu ellemeyin

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
# ssh anahtarı oluşturmak için bir linux terminalinde "ssh-keygen" yazıp,
# sonra bu anahtarı bulmak için ~/.ssh klasörüne gidip id_<anahtar-adı>.pub dosyasını açabilirsiniz. (.pub ile biten dosya olduğundan emin olun, diğeri gizli anahtar)
# Buradaki varsayılan anahtarın gizli anahtarını almak için beni okulda bulun (Çınar Mert Çeçen), yada cinar@cinarcecen.dev
ssh_public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDNIljS9EpC44CkGvbcLd/iKIHmwOsgZFMAT2bVYBtzk bartin-lisesi"

# GRUB config dosyası nerede? ("/etc/default/grub")
# Bunu gerekmedikçe değiştirmeyin.
grub_config_path = "/etc/default/grub"

# -------------------------

if __name__ == "__main__":
    print("Bu dosya doğrudan çalıştırılamaz. Lütfen main.py dosyasını çalıştırın.")
else:
    print("» Config dosyası yüklendi.")