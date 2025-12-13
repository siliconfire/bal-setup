"""
Bilgisayarın durumunu 2 dakikada bir kontrol edip, kimse giriş yapılı değilse cihazı kapatan bir systemd servisini kurar.
-- Ali Efe Aktuğ <efealiaktug@gmail.com>
-- Co-authored-by: Çınar Mert Çeçen <cinar@cinarcecen.dev>
"""

import tempfile
from pathlib import Path
from utils import output2 as output, action2 as action, run

def setup():
    # Welcome text (kept exactly as original)
    output("Akıllı Kapat kurulumuna hoş geldiniz.")
    output("")

    # 1. Kontrol betiğini oluştur (/usr/local/bin altına)
    output("script yazılıyor...")

    akilli_script = r"""#!/bin/bash
while true; do
    # 2 dakikada bir kontrol edip, kimse giriş yapılı değilse tahtayı kapatan script
    # systemd servisinin adı "akilli_kapat.service" olmalı
    # -- Ali Efe Aktuğ <efealiaktug@gmail.com>
    # -- Co-authored-by: Çınar Mert Çeçen <cinar@cinarcecen.dev>

    # 120 saniye bekle
    sleep 120

    # users komutu boşsa (0), cihazı kapat
    if [ $(users | wc -w) -eq 0 ]; then
        /usr/sbin/shutdown -h now
    fi
done
"""

    # Write the script to a temporary file first
    tmp_dir = tempfile.gettempdir()
    tmp_script_path = Path(tmp_dir) / "akilli_kapat.sh.tmp"
    with open(tmp_script_path, "w", encoding="utf-8") as f:
        f.write(akilli_script)

    # Use utils.action to copy the file into place with proper permissions (avoids shell redirection/pipes)
    # install will copy the file and set the mode
    action("script yükleniyor...", f"install -m 755 {tmp_script_path} /usr/local/bin/akilli_kapat.sh")

    # 2. Çalıştırma izni ver
    # chmod is redundant because install set the mode, but we keep it for parity with original script
    action("chmod +x...", "chmod +x /usr/local/bin/akilli_kapat.sh")

    # 3. Systemd servisi oluştur
    output("systemd servisi oluşturuluyor...")

    service_unit = r"""[Unit]
Description=Akıllı Tahta Otomatik Kapatma Servisi
After=network.target

[Service]
ExecStart=/usr/local/bin/akilli_kapat.sh
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""

    tmp_service_path = Path(tmp_dir) / "akilli_kapat.service.tmp"
    with open(tmp_service_path, "w", encoding="utf-8") as f:
        f.write(service_unit)

    action("servis dosyası kopyalanıyor (/etc/systemd/system/akilli_kapat.service)...", f"install -m 644 {tmp_service_path} /etc/systemd/system/akilli_kapat.service")

    # 4. Servisi aktif et ve başlat
    output("systemd servisi başlatılıyor...")
    action("systemctl reload...", "systemctl daemon-reload")
    action("servis aktifleştiriliyor...", "systemctl enable akilli_kapat.service")
    action("servis başlatılıyor...", "systemctl start akilli_kapat.service")

    # Kurulum bitti uyarısı (Sadece bir kez kurulum anında görünür)
    output("")
    output("Kurulum tamamlandı.")
    output("görüşürüz.")
    output("")

    # notify-send ui gerektrirebilir, sudo ile çalıştıralım
    run("notify-send \"Kurulum Tamamlandı\" \"Otomatik kapatma servisi başarıyla kuruldu ve başlatıldı.\"", sudo=False)

    # Cleanup temporary files
    output("temizlik yapılıyor...")
    try:
        tmp_script_path.unlink()
    except Exception:
        pass
    try:
        tmp_service_path.unlink()
    except Exception:
        pass


if __name__ == "__main__":
    output("Dosya direkt olarak çalıştırıldı, sadece servis kurulumunu yapıyorum. (Tam kurulum için main.py'ı kullanın!!)")
    setup()
else:
    print("» Alinin otomatik kapatma scripti yüklendi.")