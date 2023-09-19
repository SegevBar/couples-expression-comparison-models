#!/bin/bash
# file adapted from MICA https://github.com/Zielon/MICA/
cd spectre_model
urle () { [[ "${1}" ]] || return 1; local LANG=C i x; for (( i = 0; i < ${#1}; i++ )); do x="${1:i:1}"; [[ "${x}" == [a-zA-Z0-9.~-] ]] && echo -n "${x}" || printf '%%%02X' "'${x}"; done; echo; }

echo "Download FLAME model"
username=$("segevbar94@gmail.com")
password=$("FLAME23CrAdc")
mkdir -p data/FLAME2020/
wget --post-data "username=$username&password=$password" 'https://download.is.tue.mpg.de/download.php?domain=flame&sfile=FLAME2020.zip&resume=1' -O './FLAME2020.zip' --no-check-certificate --continue
unzip FLAME2020.zip -d data/FLAME2020/
rm -rf FLAME2020.zip

echo -e "\nDownload pretrained SPECTRE model..."
gdown --id 1vmWX6QmXGPnXTXWFgj67oHzOoOmxBh6B
mkdir -p pretrained/
mv spectre_model.tar pretrained/


