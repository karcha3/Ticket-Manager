<p align="center"><img src="docs/icon.png" alt="" width="72"></p>

# Ticket Manager

**Keep track of the event tickets you hold: who they're for, the event, the seat, the date,
the price and the status, all in one searchable list.** Apps for Windows, Linux and Android.

Website: https://karcha3.github.io/ticketmanager ·
[Privacy](https://karcha3.github.io/ticketmanager/privacy.html) ·
[Terms](https://karcha3.github.io/ticketmanager/terms.html)

![Ticket Manager window](docs/screenshot.png)

## Download

Get the latest files from the [Releases page](https://github.com/karcha3/Ticket-Manager/releases/).

| App | File | Notes |
| --- | --- | --- |
| Windows (installer, recommended) | [TicketManager-Setup-Windows-1.0.exe](https://github.com/karcha3/Ticket-Manager/releases/download/V1.0-Build1.2/TicketManager-Windows-Setup-1.0.exe) | Setup wizard, Start menu shortcut, optional desktop shortcut, uninstaller. Windows 10 or 11, 64-bit. |
| Windows (portable) | [TicketManager-Portable-Windows-1.0.exe](https://github.com/karcha3/Ticket-Manager/releases/download/V1.0-Build1.2/TicketManager-Windows-Portable-1.0.exe) | Runs without installing. Not the full installation. |
| Linux | [TicketManager-Linux-1.0-x86_64.AppImage](https://github.com/karcha3/Ticket-Manager/releases/download/V1.0-Build1.2/TicketManager-Linux-1.0-x86_64.AppImage) | 64-bit PCs. See [Linux](#linux). |
| Android | [TicketManager-Android-1.0.apk](https://github.com/karcha3/Ticket-Manager/releases/download/V1.0-Build1.2/Ticket-Manager-Android-Phone_1.0.apk) | Android 8.0 or newer. See [Android](#android). |

## Features (Windows and Linux)

- Add, edit, duplicate and delete tickets
- Fields for first and last name, venue type, ticket type, venue or event, location, date,
  time, seat or section, price, status and notes
- Calendar and clock pickers for dates and times
- A tab for each venue, created automatically as you add tickets
- Live search across all fields; click a column header to sort; double-click a row to edit
- Export to CSV (exports what you currently see, including your search and venue tab)
- Import tickets from an exported CSV (rows already in the app are skipped)
- Optional sync between your devices (see [Sync](#sync-optional))
- Light and dark mode, remembered between launches
- A status bar with your ticket count and the total price of your tickets, not counting
  cancelled or refunded ones

## Android

A native Android app (Kotlin, Jetpack Compose) with the same tickets and fields.

- Add, edit, duplicate and delete tickets, with a calendar picker and a clock picker
- Search, and a tab for each venue; total price in the status bar
- Import a CSV from any of the apps, and export what you see
- Sync with the other apps
- **Codes and scanning (Android only):** show a ticket's code as a QR code or a Code 128
  barcode, scan a code to check a ticket and mark it as used, or scan a real ticket's code
  into the ticket. Checks only use the tickets on that phone, and codes made by the app are for
  your own bookkeeping, not for entry at a venue.
- Light and dark mode that follows the phone
- The only permission it asks for is internet access, used only when you choose
  "Sync with Google". The scanner is Google's code scanner and needs Google Play services.

## Linux

```
chmod +x TicketManager-1.0-x86_64.AppImage
./TicketManager-1.0-x86_64.AppImage
```

- If it asks for FUSE: `sudo apt install libfuse2` (`libfuse2t64` on Ubuntu 24.04), or run it with
  `--appimage-extract-and-run`.
- If it does not start and mentions the Qt "xcb" plugin:
  `sudo apt install libxcb-cursor0 libegl1 libxkbcommon-x11-0`.
- Google Drive has no official Linux app, so for sync-file syncing use a folder kept in sync by
  Dropbox, Nextcloud, Syncthing, or Google Drive through `rclone mount` or Insync.

## Your data

| App | Where tickets are stored |
| --- | --- |
| Windows | `%APPDATA%\TicketManager` |
| Linux | `~/.local/share/TicketManager` |
| Android | the app's private storage |

Nothing is uploaded unless you turn on sync. Updating or uninstalling does not delete your
tickets. Use **Export CSV** to make a backup.

## Sync (optional)

Sync is off until you turn it on. It is manual and the newest edit of each ticket wins
(keep your devices' clocks correct); deletions sync too. Two ways:

- **Sign in with Google:** your tickets are kept in a hidden app-data folder in your own Google
  Drive (the app can see only that file, not the rest of your Drive). You use your own free
  Google Cloud credentials, entered once in the app: see **[GOOGLE-SETUP.md](GOOGLE-SETUP.md)**.
  On the PC: right-click **Sync**. On Android: **More → Sync with Google**.
- **A sync file:** pick a file in a folder that your cloud service keeps in sync. The app only reads
  and writes that file. On the PC: click **Sync**. On Android: **More → Sync: create new sync file**.

The same sync data works across all the apps.

## Good to know

- Windows SmartScreen may show "Windows protected your PC" the first time you run the app.
  Click **More info**, then **Run anyway**.
- Installing the Android `.apk` from outside an app store needs your permission: allow installs from
  your browser or file manager when asked. Google Play Protect may show a warning for apps from
  developers it does not know.
- The first launch of the portable Windows version can be slow, because it unpacks itself.
- The release `.apk` is signed with the standard debug key, which is fine for installing directly.

## Building from source

Python 3.12 (64-bit) is needed for the Windows and Linux apps.

**Run from source:**
```
pip install -r requirements.txt
python main.py
```

**Windows installer:** install [Inno Setup 6.3+](https://jrsoftware.org/isdl.php), tick "Add
python.exe to PATH" when installing Python, then double-click `build_windows.bat`. You get
`dist\TicketManager.exe` and `installer_output\TicketManager-Setup-1.0.exe`.

**Linux AppImage:** on Linux run `bash build_linux.sh` (needs internet). You get
`installer_output/TicketManager-1.0-x86_64.AppImage`. Build on an older distribution such as
Ubuntu 22.04 so it also runs on older systems.

**Android:** install Android Studio, open the `android` folder, let Gradle sync, then
**Build → Build APK(s)**.

**Tests** (no screen needed):
```
python -m unittest discover -s tests -v
```

### Making a release

GitHub builds everything for you. Push a tag:
```
git tag v1.0
git push origin v1.0
```
The **Build release** workflow builds the Windows installer and portable exe, the Linux AppImage
and the Android APK, and creates a **draft** release with the files attached. Check it, add the
release notes, and publish. The version number comes from the tag.

### Publishing the website

The website is in the `docs` folder. In the repository go to **Settings → Pages**, choose
**Deploy from a branch**, branch `main`, folder `/docs`.

## Project layout

```
main.py             entry point
main_window.py      main window (tabs, table, search, import/export, sync)
ticket_dialog.py    add/edit ticket dialog
database.py         SQLite storage, CSV import/export, sync merge
google_sync.py      Google sign-in and Google Drive sync
styles.py           light and dark themes
pickers.py          calendar and clock popups
resources.py        file paths (source and built app)
ui/                 Qt Designer layouts
assets/             app icons
tests/              automated tests
installer/          Inno Setup script (Windows installer)
android/            Android app (Kotlin, Jetpack Compose, Room)
docs/               the website (GitHub Pages)
.github/            issue templates and build workflows
```

## More

[Changelog](CHANGELOG.md) · [Security policy](SECURITY.md) · [Contributing](CONTRIBUTING.md) ·
[Google sync setup](GOOGLE-SETUP.md)

## License

Copyright (c) 2026 Karcha Studios. All rights reserved. See [LICENSE.txt](LICENSE.txt). It covers
the Windows, Linux and Android apps. The source is visible for viewing only; copying, modifying and
redistributing it is not permitted.

Third-party components (for example Qt for Python, AndroidX, ZXing and Google's code scanner)
remain under their own licenses.
