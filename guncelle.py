#!/usr/bin/env python3
"""Raspberry Pi OS'u otomatik günceller ve yükseltir.

Çalıştırılacak komutlar:
    sudo apt update
    sudo apt full-upgrade -y
"""
import os
import subprocess
import sys

KOMUTLAR = [
    ["apt", "update"],
    ["apt", "full-upgrade", "-y"],
]


def main():
    prefix = [] if os.geteuid() == 0 else ["sudo"]
    env = dict(os.environ, DEBIAN_FRONTEND="noninteractive")
    for komut in KOMUTLAR:
        tam = prefix + komut
        print("Çalıştırılıyor: " + " ".join(tam), flush=True)
        try:
            sonuc = subprocess.run(tam, env=env if not prefix else None)
        except FileNotFoundError as e:
            print("Komut bulunamadı: %s" % e.filename, file=sys.stderr)
            return 1
        if sonuc.returncode != 0:
            print("Hata: komut %d koduyla bitti." % sonuc.returncode, file=sys.stderr)
            return sonuc.returncode
    print("Güncelleme ve yükseltme tamamlandı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
