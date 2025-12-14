import os
import subprocess
import sys

dry = True


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
    return github_repo, github_branch


def fetch_file_list(github_repo: str, github_branch: str):
    download_file("file_list.txt", github_repo, github_branch)
    with open("file_list.txt.tmp_new", "r") as f:
        file_list = f.read().splitlines()
    print("\n[+] | Güncellenecek dosyalar:")
    print(f"    | {file_list}\n")
    return file_list

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

    # temizle
    for file_name in file_list:
        temp_file_name = file_name + ".tmp_new"
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

if "__main__" == __name__:
    print("Hoşgeldiniz. Güncelleme aracını başlatıyorum...")
    main()
