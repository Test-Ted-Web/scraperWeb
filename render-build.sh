#!/usr/bin/env bash
# Salir si hay errores
set -o errexit

pip install -r requirements.txt

# Instalar Google Chrome
STORAGE_DIR=/opt/render/project/.render

if [ ! -d "$STORAGE_DIR/chrome" ]; then
  echo "...Instalando Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P . https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x google-chrome-stable_current_amd64.deb .
else
  echo "...Chrome ya está instalado"
fi
