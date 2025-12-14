import getpass
import os
import subprocess
import sys

dry = False  # fake atması (dry run) için True yapın.


def pull_variables():
    """Neden böyle saçma bir fonksiyon yazdığımı düşünüyor olabilirsiniz, açıklayayım.
    Eğer config varsa değerleri ordan çekmek istiyorum (ki kullanıcı değiştirebilsin), ama eğer config yoksa kullanıcıları "değersiz" bırakmak istemiyorum.
    Kullanıcının bu repoyu tamamen bu update.py dosyası ile çekeceğini değerlendirince çok da saçma gelmiyor."""
    try:
        from config import github_repo, github_branch
        print(f"\n[+] | Config dosyanızdan adresi çektim...")
        print(f"    | {github_repo} ({github_branch})")
    except ImportError:
        github_repo = "siliconfire/bal-setup"
        github_branch = "master"
        print(
            "\n[!] | Config dosyanız yok herhalde, bu ilk kurulum ise bu tamamen normal. Varsayılan değerleri kullanıyorum...")
        print(f"    | {github_repo} ({github_branch})")
        download_config_too = True
    return github_repo, github_branch


def run(command: str, sudo: bool = True):
    """utils.py zamanında hazır olmayabileceği için bu fonksiyonu direkt olarak update.py dosyasına koydum.
    evet biliyorum, aynı kod 2 yerde geçiyor, berbat biriyim falan. umrumda değil."""
    if sudo:
        command = "sudo -S " + command
    if dry:
        print(f"[DRY RUN] {command}")
        return
    command = command.split()
    subprocess.run(command)


def download_file(file_name: str, github_repo: str, github_branch: str, failed_before: bool = False):
    """belirtilen dosyayı githubdan indirir. inşallah indirecek. bilmiyorum genelde dua etmek yardımcı oluyor.
    önce curl ile deneriz, olmazsa apt üzerinden curl kurup tekrar deneriz, yoksa hata verir çıkarız.."""
    file_url = f"https://raw.githubusercontent.com/{github_repo}/{github_branch}/{file_name}"
    temp_file_name = file_name + ".tmp_new"
    curl_command = f"curl -#L -o {temp_file_name} {file_url}"

    print(f"[+] | {file_name} dosyasını indiriyorum...")
    try:
        run(curl_command)
    except:  # noqa, seninle mi uğraşacam ya.
        if failed_before:
            print(f"\n[!] | ikinci kere {file_name} dosyasını indiremedim. internetini kontrol et.")
            print("    | kapatıyorum görüşürüz.")
            sys.exit(1)
        else:
            print("\n[!] | curl ile indirme başarısız oldu. ya curl yüklü değildir yada internet yoktur.")
            print("    | ben bi curl yüklemeyi deneyeyim...")
            run("apt install -y curl")
            print("    | yüklenme işlemi bitti, tekrar deniyorum...")
            download_file(file_name, github_repo, github_branch, True)


def check_file(temp_file_name: str):
    """belirtilen dosyanın var olup olmadığını kontrol eder. yoksa hata verip çıkar."""
    if dry:
        return True
    if not os.path.exists(temp_file_name) or os.path.getsize(temp_file_name) == 0:
        print(f"[!] | dosya {temp_file_name} indirildi fakat varlık kontolünden geçemedi.")
        print("    | bu hata muhtemelen benim tarafımda. (Çınar Mert Çeçen, cinar@cinarcecen.dev)")
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
        return False
    return True


def replace_file(old, new):
    """eski dosyayı yeni dosyayla değiştirir."""
    print(f"[»] | {old} » {new}...")
    if dry:
        return
    os.replace(old, new)


def fetch_file_list(github_repo: str, github_branch: str):
    """dosya listesini çeker."""
    download_file("file_list.txt", github_repo, github_branch)
    if dry:
        file_list = ["file1.txt", "file2.txt", "example.py"]
    else:
        with open("file_list.txt.tmp_new", "r") as f:
            file_list = f.read().splitlines()
    print("\n[+] | Güncellenecek dosyalar:")
    print(f"    | {file_list}\n")
    return file_list

def cleanup(file_name):
    if dry:
        pass
    temp_file_name = file_name + ".tmp_new"
    if os.path.exists(temp_file_name):
        os.remove(temp_file_name)
    if os.path.exists("file_list.txt.tmp_new"):
        os.remove("file_list.txt.tmp_new")

def fix_perms(file_name: str):
    """belirtilen dosyanın izinlerini düzeltir."""
    username = getpass.getuser()
    print(f"[+] | {file_name} dosyasının sahibi {username} yapılıyor...")
    if not dry:
        run(f"chown -R {username}:{username} {file_name}", sudo=True)

    print(f"[+] | {file_name} dosyasının yetkileri 755 yapılıyor...")
    if not dry:
        run(f"chmod -R 755 {file_name}", sudo=True)


def main():
    github_repo, github_branch = pull_variables()

    print("\n[+] | Güncellenecek dosya adları çekiliyor...")
    file_list = fetch_file_list(github_repo, github_branch)
    # indir
    for file_name in file_list:
        download_file(file_name, github_repo, github_branch)

    # yerleştir
    for file_name in file_list:
        temp_file_name = file_name + ".tmp_new"
        if check_file(temp_file_name):
            replace_file(temp_file_name, file_name)
        else:
            print("[!] | güncelleme tamamlanamadı. kapatıyorum görüşürüz.")
            sys.exit(1)
    print()

    # temizle
    for file_name in file_list:
        cleanup(file_name)
    print()

    # yetkileri düzelt
    for file_name in file_list:
        fix_perms(file_name)

    print("\n\n" + "-"*20 + "\n")
    print("[+] | Güncelleme tamamlandı. Görüşürüz.")


def check_updates():
    """güncelleme olup olmadığını kontrol eder."""
    global download_config_too
    print("[+] | Güncelleme kontrolü yapıyorum...")
    try:
        with open("version", "r") as f:
            ver = f.read()
    except FileNotFoundError:
        print("\n[!] | Versiyon dosyanız yok, muhtemelen bu ilk kurulumunuz. Hoşgeldiniz.")
        print("    | Güncelleme başlatıyorum.")
        download_config_too = True
        return True
    else:
        print("[+] | Versiyon dosyanız var.")

    try:
        from config import github_repo, github_branch
    except ModuleNotFoundError:
        print("\n[!] | Config dosyanız yok. onu bi indirelim.")
        print("    | Güncelleme başlatıyorum.")
        download_config_too = True
        return True
    else:
        print("[+] | Config dosyanız var.")

    download_file("version", github_repo, github_branch)
    if dry:
        return True
    with open("version.tmp_new", "r") as f:
        latest_ver = f.read()
    if latest_ver > ver:
        print("[!] | Sunucuda daha yeni bir sürüm var.")
        print("    | GÜncelleme başlatıyorum.")
        return True
    return False

if "__main__" == __name__:
    print("Güncelleme kontrolcüsüne hoşgeldiniz.")
    download_config_too = False
    while True:
        print(f"""
[1] Programı güncelle (güncelleme var ise yapar ve gerekenleri indirir, yoksa yapmaz)
[2] Zorla güncelle (güncelleme olsa da olmasa da güncelleme yapar)
[3] Sürümü kontrol et (yeni sürüm var mı?)

[8] Çalışıyor gibi yap, gerçekten birşey yapma ({dry})
[9] Config dosyamı da sıfırla ({download_config_too})

""")
        choice = input("Seçiminiz: ")

        if choice == "1":
            if check_updates():
                main()
            else:
                print("\n[+] | Zaten en son sürümü kullanıyorsunuz. Güncelleme yapmıyorum.")
            break
        elif choice == "2":
            main()
            break
        elif choice == "3":
            if check_updates():
                print("\n[!] | Yeni sürüm mevcut.")
            else:
                print("\n[+] | Zaten en son sürümü kullanıyorsunuz.")
            break
        elif choice == "8":
            dry = not dry
        elif choice == "9":
            download_config_too = not download_config_too
        else:
            print("\n" + "-"*20 + "\nYanlış seçim yaptınız. Lütfen istediğiniz rakamı girip ENTER tuşuna basın.")