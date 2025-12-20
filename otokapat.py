"""
Bilgisayarın durumunu 2 dakikada bir kontrol edip, kimse giriş yapılı değilse cihazı kapatan bir systemd servisini kurar.
-- Ali Efe Aktuğ <efealiaktug@gmail.com>
-- Co-authored-by: Çınar Mert Çeçen <cinar@cinarcecen.dev>
"""

import tempfile
from pathlib import Path
from utils import output2 as output, action2 as action, run

def setup():
    output("Akıllı Kapat kurulumuna hoş geldiniz.")
    output("")

    # 1. Kontrol betiğini oluştur (/usr/local/bin altına)
    output("script yazılıyor...")

    akilli_script = r"""#!/bin/bash
# Tek seferlik kontrol: kimse giriş yapılı değilse cihazı kapatır.
# Zamanlama systemd timer tarafından yönetilir.

# users komutu boşsa (0), cihazı kapat
if [ $(users | wc -w) -eq 0 ]; then
    # Kapatma komutunu çalıştırmadan önce loglama yapılabilir.
    /usr/sbin/shutdown -h now
    exit 0
fi
exit 0
"""

    # önce geçici dosyaya yaz
    tmp_dir = tempfile.gettempdir()
    tmp_script_path = Path(tmp_dir) / "akilli_kapat.sh.tmp"
    with open(tmp_script_path, "w", encoding="utf-8") as f:
        f.write(akilli_script)

    # DÜZGÜN YETKİLERLE kopyalayalım (inşallah)
    action("script yükleniyor...", f"install -m 755 {tmp_script_path} /usr/local/bin/akilli_kapat.sh")

    # çalıştırma izni ver
    action("chmod +x...", "chmod +x /usr/local/bin/akilli_kapat.sh")

    # systemd servisini oluştur
    output("systemd servisi oluşturuluyor...")

    service_unit = r"""[Unit]
Description=Akıllı Tahta Otomatik Kapatma Servisi
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/akilli_kapat.sh
User=root

[Install]
WantedBy=multi-user.target
"""
    tmp_service_path = Path(tmp_dir) / "akilli_kapat.service.tmp"
    with open(tmp_service_path, "w", encoding="utf-8") as f:
        f.write(service_unit)

    action("servis dosyası kopyalanıyor (/etc/systemd/system/akilli_kapat.service)...", f"install -m 644 {tmp_service_path} /etc/systemd/system/akilli_kapat.service")

    # 4. sytemd zamanlayıcısını oluştur
    output("systemd zamanlayıcı (timer) oluşturuluyor...")

    timer_unit = r"""[Unit]
Description=Akıllı Tahta Otomatik Kapatma Zamanlayıcısı

[Timer]
# 2 dakikada bir çalıştır
OnUnitActiveSec=2min
Unit=akilli_kapat.service

[Install]
WantedBy=timers.target
"""
    tmp_timer_path = Path(tmp_dir) / "akilli_kapat.timer.tmp"
    with open(tmp_timer_path, "w", encoding="utf-8") as f:
        f.write(timer_unit)

    action("timer dosyası kopyalanıyor (/etc/systemd/system/akilli_kapat.timer)...", f"install -m 644 {tmp_timer_path} /etc/systemd/system/akilli_kapat.timer")

    # 5. daemon reload
    output("systemd zamanlayıcı başlatılıyor...")
    action("systemctl reload...", "systemctl daemon-reload")

    # zamanlayıcıyı başlat (servisi değil!!!!!!!!!!!!)
    action("zamanlayıcı aktifleştiriliyor...", "systemctl enable akilli_kapat.timer")
    action("zamanlayıcı başlatılıyor...", "systemctl start akilli_kapat.timer")

    # end
    output("")
    output("Kurulum tamamlandı.")
    output("görüşürüz.")
    output("")

    # notify-send ui gerektrirebilir, ne olur bilmiyorum
    # sudosuz calistiralim ki, bende bilmiyorum aslında nedenini, gerek yok ama.
    # relax olacan biraz bu hayatta.
    run("notify-send \"Kurulum Tamamlandı\" \"Otomatik kapatma servisi başarıyla kuruldu ve başlatıldı.\"", sudo=False, shell=True)

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
    try:
        tmp_timer_path.unlink()
    except Exception:
        pass


if __name__ == "__main__":
    output("Dosya direkt olarak çalıştırıldı, sadece servis kurulumunu yapıyorum. (Tam kurulum için main.py'ı kullanın!!)")
    setup()
else:
    print("» Alinin otomatik kapatma scripti yüklendi.")