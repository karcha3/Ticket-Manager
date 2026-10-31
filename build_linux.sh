#!/usr/bin/env bash
# Builds TicketManager-<version>-x86_64.AppImage on Linux.
# Run from the project folder (the one with main.py):  bash build_linux.sh
set -euo pipefail
cd "$(dirname "$0")"

VERSION="1.0"
PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python 3 was not found. Install it first, for example: sudo apt install python3 python3-venv"
  exit 1
fi
missing=0
for f in main.py main_window.py ticket_dialog.py database.py styles.py pickers.py resources.py ui_loader.py google_sync.py \
         ui/mainwindow.ui ui/ticketdialog.ui assets/icon.png \
         ticket_manager_linux.spec AppRun ticketmanager.desktop; do
  if [ ! -e "$f" ]; then echo "Missing file: $f"; missing=1; fi
done
if [ "$missing" = "1" ]; then
  echo "Run this from the project folder, put the .ui files in a 'ui' folder, and copy the linux-appimage files into it."
  exit 1
fi

echo "== Creating virtual environment (.venv-linux) =="
"$PYTHON" -m venv .venv-linux
# shellcheck disable=SC1091
source .venv-linux/bin/activate
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; else python -m pip install "PySide6>=6.5"; fi
if [ -f requirements-build.txt ]; then python -m pip install -r requirements-build.txt; else python -m pip install "pyinstaller>=6.6"; fi

echo "== Building the app folder with PyInstaller =="
python -m PyInstaller ticket_manager_linux.spec --noconfirm --distpath dist-linux --workpath build-linux

echo "== Assembling AppDir =="
rm -rf AppDir
mkdir -p AppDir/usr/bin
cp -r dist-linux/TicketManager AppDir/usr/bin/
cp AppRun AppDir/AppRun
chmod +x AppDir/AppRun
cp ticketmanager.desktop AppDir/ticketmanager.desktop
cp assets/icon.png AppDir/ticketmanager.png
ln -sf ticketmanager.png AppDir/.DirIcon
[ -f LICENSE.txt ] && cp LICENSE.txt AppDir/LICENSE.txt

echo "== Getting appimagetool =="
TOOL="./appimagetool-x86_64.AppImage"
if [ ! -x "$TOOL" ]; then
  URL="https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"
  if command -v curl >/dev/null 2>&1; then curl -L -o "$TOOL" "$URL"; else wget -O "$TOOL" "$URL"; fi
  chmod +x "$TOOL"
fi

echo "== Building the AppImage =="
mkdir -p installer_output
ARCH=x86_64 APPIMAGE_EXTRACT_AND_RUN=1 "$TOOL" AppDir "installer_output/TicketManager-${VERSION}-x86_64.AppImage"

echo
echo "Done: installer_output/TicketManager-${VERSION}-x86_64.AppImage"
