# Ticket Manager

A desktop ticket-management app built with **PySide6** (Qt for Python),
structured as a proper Qt Creator project.

## Project layout

```
ticket_manager.pyproject   ← open this in Qt Creator
main.py                    ← entry point
main_window.py             ← main window logic (tabs, table, search, export)
ticket_dialog.py           ← add/edit ticket dialog logic
database.py                ← SQLite storage + CSV export
styles.py                  ← light / dark QSS themes
ui_loader.py                ← tiny helper that loads .ui files at runtime
pickers.py                  ← calendar & clock-dial popup pickers
resources.py                ← resolves bundled files + writable data folder
                               (works both from source and from the built .exe)
ui/mainwindow.ui           ← toolbar + tabs + status bar layout (edit in Designer)
ui/ticketdialog.ui         ← add/edit ticket form layout (edit in Designer)
assets/icon.png             ← app icon (window icon)
assets/icon.ico             ← app icon (Windows exe icon)
ticket_manager.spec         ← PyInstaller build config
build_windows.bat           ← one-click build script for Windows
requirements.txt
requirements-build.txt      ← adds PyInstaller, only needed to build the exe
```

## Opening in Qt Creator

1. Open Qt Creator → **File > Open File or Project...**
2. Select `ticket_manager.pyproject`.
3. Qt Creator will list all the project files in the sidebar. Double-click
   `ui/mainwindow.ui` or `ui/ticketdialog.ui` to edit the layouts visually
   in the built-in **Designer**.
4. To run it, set up a Python interpreter for the project (Qt Creator will
   prompt you), or just run it from a terminal as below.

## Running from the command line

```bash
pip install -r requirements.txt
python main.py
```

Requires Python 3.9+.

The `.ui` files are loaded at runtime with `QUiLoader`, so there is no
build/compile step — editing a `.ui` file in Designer and re-running the
app is enough to see your changes.

## Building a Windows .exe

You need to build **on Windows** — PyInstaller doesn't cross-compile, so
running the build on Linux/macOS would not produce a working Windows exe.

**Easiest way:**

1. Copy this whole folder onto a Windows machine (with Python 3.9+ installed).
2. Double-click `build_windows.bat` (or run it from Command Prompt).
   It creates a virtual environment, installs everything, and runs
   PyInstaller for you.
3. When it finishes, your app is at `dist\TicketManager.exe` — a single
   file with the ticket icon baked in, no console window, no Python
   install required on the machine you copy it to.

**Manual way**, if you'd rather run the steps yourself:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-build.txt
pyinstaller ticket_manager.spec
```

The resulting `dist\TicketManager.exe` is portable — copy it anywhere,
or zip up the whole `dist` folder to share with someone else. It doesn't
need Qt Creator, Python, or PySide6 installed on the target machine.

A couple of things worth knowing:
- The **first run** of a onefile exe is a bit slower than later runs,
  since it unpacks itself into a temp folder each time it starts.
- If you ever want a faster-starting build instead (a folder of files
  rather than one exe), run `pyinstaller ticket_manager.spec --onedir`
  style tweaks, or ask and I can add a onedir variant.
- macOS/Linux builds work the same way (`pyinstaller ticket_manager.spec`
  on that OS gives you a `.app` or a Linux binary respectively) — just
  skip `build_windows.bat` and run the manual commands above on that OS.

## Features

- **Fields**: venue type (dropdown), ticket type (dropdown), first/last
  name, venue/event name (dropdown, pre-filled with venues you've already
  used, editable for new ones), location, date, time, seat/section, price,
  status (dropdown), notes.
- **Date & time pickers**: the date field has both the standard calendar
  dropdown and a dedicated 📅 button that opens a full calendar popup —
  click a day to set it. The time field has a dropdown of 30-minute slots
  plus a 🕐 button that opens a clock-style popup with an hour dial and a
  minute dial; turn them and hit Done.
- **Duplicate**: select a ticket and click "⧉ Duplicate" to open a new
  ticket pre-filled with all of its details — handy for buying several
  tickets to the same event, just tweak the name/seat and save.
- **Tabs per venue**: an "All Venues" tab plus one auto-generated tab per
  distinct venue name, so you can quickly flip between events. Tabs update
  automatically as you add/edit tickets. Adding a ticket while on a venue
  tab pre-fills that venue for you.
- **Search**: live filter across all fields, scoped to the active tab.
- **Export**: "Export CSV" exports whatever is currently visible in the
  active tab (respecting the search filter and venue tab), so you can
  export everything or just one event's tickets.
- **Persistence**: SQLite database (`tickets.db`) stored in a per-user
  data folder (`%APPDATA%\TicketManager` on Windows, `~/Library/Application
  Support/TicketManager` on macOS, `~/.local/share/TicketManager` on Linux)
  — every add/edit/delete commits immediately, and the connection is
  closed cleanly on exit. This location is used both when running from
  source and from the built exe, so your data survives reinstalling or
  moving the app.
- **App icon**: a ticket icon is used for the window and, once built, for
  the .exe file itself.
- **Dark mode**: toggle button in the toolbar, remembered between launches.

## Notes

- Click a column header to sort a table; double-click a row (or select +
  click "Edit") to modify a ticket.
